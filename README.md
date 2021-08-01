# reflective-potential
### An empirical analysis of Earth's reflective potential

## Introduction

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

This code repository contains a workflow to estimate the potential of Earth's
surface to reflect incoming sunlight back out to space. It uses data from the
fifth European Centre for Medium-Range Weather Forecasts
(ECMWF) reanalysis product (ERA5), specifically radiative fluxes at the surface
and top of atmosphere. This allows us to estimate surface reflectance and
atmospheric transmittance and reflectance. When averaged over several decades,
these properties can be combined with incoming solar radiation to model the
potential surface-reflected outgoing solar radiation:

![ROM](https://github.com/ReflectiveEarth/reflective-potential/blob/main/assets/ROM_v030.png)

## Developer Setup

1. Clone and change directory to the reflective-potential repo.
  * `git clone https://github.com/ReflectiveEarth/reflective-potential.git`
  * `cd reflective-potential`
1. Create and activate the conda environment corresponding to the notebook you would like to run.
  * e.g. Conda environment for `01-ingest.ipynb`
    * `conda create --file environment.ingest.yml`
    * `conda activate ingest`
1. Launch Jupyter Lab.
  * `jupyter lab`
1. Open and run any of the notebooks in the eponymous directory.
  * N.B. additional setup may be required. See the *Preliminaries* section of
    each notebook.

## Prerequisites

* A Google Account in order to access Google Cloud Platform.
* A Google Cloud project with billing enabled.
* A Cloud Storage bucket to store project data.
* A Copernicus Climate Data Store Account.
* conda, either [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html).
