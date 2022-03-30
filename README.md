# reflective-potential

### An empirical analysis of Earth's surface reflectivity potential

> Contains modified [Copernicus Climate Change Service][copernicus]
> information obtained in 2021. Neither the European Commission nor
> ECMWF is responsible for any use that may be made of the Copernicus
> information or data it contains.

Reflective Earth is on a mission to slow global warming as fast and safely as
possible by increasing Earth's reflectivity to reduce its energy imbalance.
Reflectivity interventions reduce the amount of sunlight absorbed by the Earth
system, i.e. the amount of energy entering the system. Deploying reflective
materials as a stop gap could limit the amount of warming experienced by people
and buy society time to reduce greenhouse gas emissions and drawdown atmospheric
greenhouse gas concentrations.

The potential of reflective materials to reflect sunlight strongly depends on
location. The amount of incoming solar radiation varies greatly, with more
being received in the tropics and less being received at the poles. Clouds,
water vapor, and aerosols (e.g. dust, smoke) scatter and absorb sunlight. These
properties vary spatially as well.

This code repository contains workflows to estimate the potential of Earth's
surface to reflect incoming sunlight back out to space. We use data from the
European Centre for Medium-Range Weather Forecasts (ECMWF) fifth generation
reanalysis product (ERA5) and National Aeronautics and Space Administration
(NASA) Clouds and the Earth's Radiant Energy System (CERES) Energy Balanced
and Filled (EBAF) satellite-derived product, specifically radiative fluxes at
the surface and top of atmosphere. This allows us to estimate surface
reflectance and atmospheric transmittance and reflectance. When averaged over
several decades, these properties can be combined with incoming solar radiation
and surface albedo to model the potential surface-reflected outgoing solar
radiation:

![ROM][rom]

## Repository Structure

* `assets` - deliverable data and images
* `environments` - conda / mamba environment files for macOS and linux
* `notebooks` - jupyter notebooks for each step of the workflow
  * `01-Ingest` - data download from Copernicus Climate Change Service and
    upload to Google Cloud
  * `02-Preprocess` - data averaging from hourly-means to annual-means
  * `03-Analyze` - data transformation through a simple model of reflected
    radiation
  * `04-Validate` - replicate results with an independent dataset
  * `05-Visualize` - data visualization for publication
  * `utils.py` - utility functions
* `CHANGELOG` - chronologically ordered list of notable changes
* `CODE_OF_CONDUCT` - the code of conduct that contributors and maintainers
  pledge to follow
* `CONTRIBUTING` - guidelines for making your own contribution to this project
* `LICENSE` - open source license
* `README` - overview, repo structure, developer setup, and prerequisites
* `SUPPORT` - guidance on how to request help with this project

## Developer Setup

1. Clone and change directory to the reflective-potential repo.
   * `git clone https://github.com/ReflectiveEarth/reflective-potential.git`
   * `cd reflective-potential`
2. Create and activate the `conda`/`mamba` environment corresponding to the
   notebook you would like to run.
   * e.g. environment for `01-ingest.ipynb`
     * `{conda | mamba} env create --file environment/{linux | macos}.ingest.environment.yml`
     * `conda activate ingest`
3. Launch Jupyter Lab.
   * `jupyter lab`
4. Open and run the  notebooks in the eponymous directory.
   * *N.B.* additional setup may be required. See the *Preliminaries* section of
     each notebook.

### Prerequisites

* A Google Account in order to access Google Cloud Platform.
* A Google Cloud project with billing enabled. *Requester Pays* is turned on for
  all Google Cloud Storage buckets in this repo. Google Cloud Storage requests
  will incur charges.
* Optionally, [conda][conda] or [mamba][mamba] to manage package dependencies.
* Optionally, one or more Google Cloud Storage buckets to store project data.
* Optionally, a Copernicus Climate Data Store Account to ingest C3S data.

## Support

Read the [support][support] guidelines for guidance on how to reach out for help
with this project.

## Contributing

We welcome contributions that improve the quality of our code and/or science.
Before you dive in, read the [contribution][contributing] guidelines.

## Code of Conduct

This project has a [code of conduct][conduct]. By interacting with this
repository, organization, or community you agree to abide by its terms.

## License

[Clear BSD][license] © 2021-2022 [Reflective Earth][author]

<!-- Definitions -->

[author]: https://www.reflectiveearth.org
[conduct]: CODE_OF_CONDUCT.md
[conda]: https://docs.conda.io/en/latest/miniconda.html
[contributing]: CONTRIBUTING.md
[copernicus]: https://climate.copernicus.eu/
[license]: LICENSE.md
[mamba]: https://mamba.readthedocs.io/en/latest/
[rom]: assets/ROM_v042.png
[support]: SUPPORT.md
