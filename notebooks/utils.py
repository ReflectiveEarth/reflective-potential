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


def compute_radiative_properties(data):
    """Compute new variables based on a model following by Salamanca et al.
    (2012) and Stephens et al. (2015).

    Salamanca, F., Tonse, S., Menon, S., Garg, V., Singh, K., Naja, M.,
    and Fischer, M. L. (2012), Top-of-atmosphere radiative cooling with
    white roofs: experimental verification and model-based evaluation.
    Environ. Res. Lett., 7. doi: 10.1088/1748-9326/7/4/044007.

    Stephens, G. L., O'Brien, D., Webster, P. J., Pilewski, P., Kato, S.,
    and Li, J. (2015), The albedo of Earth. Rev. Geophys., 53, 141–163.
    doi: 10.1002/2014RG000449.

    Specifically, compute system reflectivity, transmittance, and surface
    albedo, then use those properties to compute the reflectance and
    transmittance of a 1-layer atmosphere following the simple model following
    Salamanca et al. (2012) and Stephens et al. (2015).

    Finally, compute the surface contribution to outgoing solar radiation and
    the potential surface contribution to the outgoing solar radiation. The
    latter is defined as the solar radiation reflected by a reference surface
    with albedo = 1 surrouded by the observed surface albedo nearby. These two
    properties are of particular interest to Reflective Earth in this analysis.

    Args:
        data: xarray Dataset containing shortwave radiative fluxes at the
            surface and top of atmosphere.

    Returns:
        xarray Dataset with additional variables added.
    """
    # System properties
    data["R"] = data["tosr"] / data["tisr"]
    data["R"] = fill_nas(data["R"])
    data["R"].attrs["long_name"] = "Planetary albedo"
    data["R"].attrs["standard_name"] = "planetary_albedo"
    data["R"].attrs["units"] = "1"

    data["T"] = data["ssrd"] / data["tisr"]
    data["T"] = fill_nas(data["T"])
    data["T"].attrs["long_name"] = "Planetary transmission"
    data["T"].attrs["standard_name"] = "planetary_transmittance"
    data["T"].attrs["units"] = "1"

    data["A"] = 1 - data["R"]
    data["A"] = fill_nas(data["A"])
    data["A"].attrs["long_name"] = "Planetary absorption"
    data["A"].attrs["standard_name"] = "planetary_aborptance"
    data["A"].attrs["units"] = "1"

    data["alpha"] = data["ssru"] / data["ssrd"]
    data["alpha"].attrs["long_name"] = "Surface albedo"
    data["alpha"].attrs["standard_name"] = "surface_albedo"
    data["alpha"].attrs["units"] = "1"

    # Intrinsic properties
    data["a"] = (data["tisr"] * data["A"] - data["ssrd"] * (1 - data["alpha"])) / data["tisr"]
    data["a"] = fill_nas(data["a"])
    data["a"].attrs["long_name"] = "1-layer atmospheric absorption"
    data["a"].attrs["standard_name"] = "atmosphere_absorptance"
    data["a"].attrs["units"] = "1"

    data["r"] = data["R"] - (data["alpha"] * data["T"]) * ((1 - data["alpha"] * data["R"]) /
                                                           (1 - data["alpha"]**2 * data["T"]**2))
    data["r"] = fill_nas(data["r"])
    data["r"].attrs["long_name"] = "1-layer atmosphere reflectivity"
    data["r"].attrs["standard_name"] = "atmosphere_reflectance"
    data["r"].attrs["units"] = "1"

    data["t"] = 1 - data["r"] - data["a"]
    data["t"] = fill_nas(data["t"])
    data["t"].attrs["long_name"] = "1-layer atmospheric transmission"
    data["t"].attrs["standard_name"] = "atmosphere_transmittance"
    data["t"].attrs["units"] = "1"

    # Reflective properties
    data["srosr"] = data["tisr"] * (data["R"] - data["r"])
    data["srosr"].attrs["long_name"] = "Surface-reflected outgoing solar radiation"
    data["srosr"].attrs["standard_name"] = "toa_outgoing_shortwave_flux"
    data["srosr"].attrs["units"] = data["tisr"].attrs["units"]

    data["psrosr"] = data["tisr"] * (data["t"]**2 / (1 - (data["alpha"] * data["r"])))
    data["psrosr"].attrs["long_name"] = "Potential surface-reflected outgoing solar radiation"
    data["psrosr"].attrs["standard_name"] = "toa_outgoing_shortwave_flux"
    data["psrosr"].attrs["units"] = data["tisr"].attrs["units"]

    check_radiative_properties(data)

    return data


def check_radiative_properties(data):
    """Check radiative property data for errors.

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
    data = data.where(~np.isinf(data)).fillna(np.nan)
    data = data.where(data < 1).fillna(np.nan)
    data = data.where(data > 0).fillna(np.nan)

    return data
