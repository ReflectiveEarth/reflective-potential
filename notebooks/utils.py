from os import environ
from warnings import warn


def check_environment(name):
    """Check the current conda environment and warn if other than expected."""    
    if environ["CONDA_DEFAULT_ENV"] != name:
        warn(f"conda environment: {name} not activated." 
              "Some dependencies may not be installed.")