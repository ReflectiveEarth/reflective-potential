import os
import numpy as np
from warnings import warn
from google.cloud import storage


def check_environment(name):
    """Check the current conda environment and warn if other than expected."""    
    if os.environ["CONDA_DEFAULT_ENV"] != name:
        warn(f"conda environment: {name} not activated." 
              "Some dependencies may not be installed.")


def get_data_gcs(file_name, bucket_name, local_path=".", user_project=None):
    """Download a dataset for a single date from Google Cloud Storage.

    Args:
        file_name: file_name to download from gcs.
        bucket_name: Google Cloud Storage bucket to download from.
        local_path: optional local path to download to.
        user_project: project ID for requester pays billing.

    Returns:
        Nothing; downloads data from Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name, user_project=user_project)
    blob = bucket.blob(file_name)
    blob.download_to_filename(filename=os.path.join(local_path, file_name))


def put_data_gcs(file_name, bucket_name, local_path=".", user_project=None):
    """Upload a dataset for a single date to Google Cloud Storage.

    Args:
        file_name: name of file to upload to gcs.
        bucket_name: Google Cloud Storage bucket to upload to.
        local_path: optional local path to upload from.
        user_project: project ID for requester pays billing.

    Returns:
        Nothing; uploads data to Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name, user_project=user_project)
    blob = bucket.blob(file_name)
    blob.upload_from_filename(filename=os.path.join(local_path, file_name))


def compute_radiative_properties(dataset):
    """Compute new variables based on a model following by Salamanca et al. (2012) and
    Stephens et al. (2015).

    Salamanca, F., Tonse, S., Menon, S., Garg, V., Singh, K., Naja, M.,
    and Fischer, M. L. (2012), Top-of-atmosphere radiative cooling with
    white roofs: experimental verification and model-based evaluation.
    Environ. Res. Lett., 7. doi: 10.1088/1748-9326/7/4/044007.

    Stephens, G. L., O'Brien, D., Webster, P. J., Pilewski, P., Kato, S.,
    and Li, J. (2015), The albedo of Earth. Rev. Geophys., 53, 141–163.
    doi: 10.1002/2014RG000449.

    Specifically, compute system reflectivity, transmittance, and surface albedo, then
    use those properties to compute the reflectance and transmittance of a 1-layer
    atmosphere following the simple model following Salamanca et al. (2012) and
    Stephens et al. (2015).

    Finally, compute the surface contribution to outgoing solar radiation and the potential
    surface contribution to the outgoing solar radiation. The latter is defined as the solar
    radiation reflected by a reference surface with albedo = 1 surrouded by the observed surface
    albedo nearby. These two properties are of particular interest to Reflective Earth in this
    analysis.

    Args:
        dataset: xarray dataset containing shortwave radiative fluxes at the surface
            and top of atmosphere.

    Returns:
        xarray dataset with additional variables added.
    """
    # System properties
    dataset["R"] = dataset["tosr"] / dataset["tisr"]
    dataset["R"] = fill_nas(dataset["R"])
    dataset["R"].attrs["long_name"] = "Planetary albedo"
    dataset["R"].attrs["standard_name"] = "planetary_albedo"
    dataset["R"].attrs["units"] = "1"

    dataset["T"] = dataset["ssrd"] / dataset["tisr"]
    dataset["T"] = fill_nas(dataset["T"])
    dataset["T"].attrs["long_name"] = "Planetary transmission"
    dataset["T"].attrs["standard_name"] = "planetary_transmittance"
    dataset["T"].attrs["units"] = "1"

    dataset["A"] = 1 - dataset["R"]
    dataset["A"] = fill_nas(dataset["A"])
    dataset["A"].attrs["long_name"] = "Planetary absorption"
    dataset["A"].attrs["standard_name"] = "planetary_aborptance"
    dataset["A"].attrs["units"] = "1"

    dataset["alpha"] = dataset["ssru"] / dataset["ssrd"]
    dataset["alpha"].attrs["long_name"] = "Surface albedo"
    dataset["alpha"].attrs["standard_name"] = "surface_albedo"
    dataset["alpha"].attrs["units"] = "1"

    # Intrinsic properties
    dataset["a"] = (dataset["tisr"] * dataset["A"] - dataset["ssrd"] * (1 - dataset["alpha"])) / dataset["tisr"]
    dataset["a"] = fill_nas(dataset["a"])
    dataset["a"].attrs["long_name"] = "1-layer atmospheric absorption"
    dataset["a"].attrs["standard_name"] = "atmosphere_absorptance"
    dataset["a"].attrs["units"] = "1"

    dataset["r"] = dataset["R"] - (dataset["alpha"] * dataset["T"]) * ((1 - dataset["alpha"] * dataset["R"]) /
                                                                       (1 - dataset["alpha"]**2 * dataset["T"]**2))
    dataset["r"] = fill_nas(dataset["r"])
    dataset["r"].attrs["long_name"] = "1-layer atmosphere reflectivity"
    dataset["r"].attrs["standard_name"] = "atmosphere_reflectance"
    dataset["r"].attrs["units"] = "1"

    dataset["t"] = 1 - dataset["r"] - dataset["a"]
    dataset["t"] = fill_nas(dataset["t"])
    dataset["t"].attrs["long_name"] = "1-layer atmospheric transmission"
    dataset["t"].attrs["standard_name"] = "atmosphere_transmittance"
    dataset["t"].attrs["units"] = "1"

    # Reflective properties
    dataset["srosr"] = dataset["tisr"] * (dataset["R"] - dataset["r"])
    dataset["srosr"].attrs["long_name"] = "Surface-reflected outgoing solar radiation"
    dataset["srosr"].attrs["standard_name"] = "toa_outgoing_shortwave_flux"
    dataset["srosr"].attrs["units"] = dataset["tisr"].attrs["units"]

    dataset["psrosr"] = dataset["tisr"] * (dataset["t"]**2 / (1 - (dataset["alpha"] * dataset["r"])))
    dataset["psrosr"].attrs["long_name"] = "Potential surface-reflected outgoing solar radiation"
    dataset["psrosr"].attrs["standard_name"] = "toa_outgoing_shortwave_flux"
    dataset["psrosr"].attrs["units"] = dataset["tisr"].attrs["units"]

    check_data(dataset)

    return dataset


def check_data(data):
    """Check data for errors.

    Args:
        data: xarray Dataset with radiative properties.

    Raises:
        AssertionError: if any of the check conditions are false.
    """
    # Check for infinites
    assert data.psrosr.where(np.isinf(data.psrosr)).count() == 0
    assert data.srosr.where(np.isinf(data.srosr)).count() == 0
    assert data.t.where(np.isinf(data.t)).count() == 0
    assert data.r.where(np.isinf(data.r)).count() == 0
    assert data.a.where(np.isinf(data.a)).count() == 0
    # Check that t+r+a=1
    np.testing.assert_allclose((data.a + data.t + data.r).mean(dim="time").values,
                                np.ones((data.sizes["latitude"], data.sizes["longitude"])))


def fill_nas(data):
    """Fill in NaN for certain conditions.

    Args:
        data: xarray DataArray.

    Returns:
        xarray DataArray with zeros filled in certain conditions.
    """
    data = data.where(~np.isinf(data)).fillna(np.nan)  # fill infinite values with 0
    data = data.where(data < 1).fillna(np.nan)  # fill values greater than 1 with 1
    data = data.where(data > 0).fillna(np.nan)  # fill values less than 0 with 0

    return data