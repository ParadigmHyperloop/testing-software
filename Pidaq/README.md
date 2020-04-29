# Pidaq (Rasp Pi Data Aquisitor) 
This directory contains all code that will run on the raspberry pi in each test stand.

This includes:
* Graphical User Interfaces  
* CAN Send/Receive
* Telemetry Logging Via InfluxDB

## Directory Structure

* docker - contains a raspbian dockerfile 
* Examples - contains various examples of libraries applied in this repo
* Lib - contains all common code in installable python packages, and install script
* Services - contains documentation/config for influxdb and grafana
* UI - contains a dash application for each project

## Setup
After creating and activating up your python virtual environment:

Install third-party python dependencies

```
cd {REPO_LOCATION}/testing-software
pip install -r requirements.txt
```

Install our custom python packages
```
cd {REPO_LOCATION}/testing-software/Pidaq/Lib
pip install -e .
```

To ensure all packages were correctly installed
```
pip freeze
```

`paradigm-testing==1.0` should be visible, among all other dependencies.


## Packages
To allow simple imports, our common modules are packaged in `Lib/` and installed using python setuptools. 
The -e, or editable, flag is used. This way, when packages are edited they dont have to be reinstalled to get the most recent version of the package. After installing the "paradigm" distribution which includes all the packages in `Lib/`, a .egg-info folder is generated. This includes info about the package and is not tracked in git.

To add your common code, simply create a folder in `Lib/` and add `__init__.py`. Then, add your python modules inside this folder. Subpackages can also be added, but `__init__.py` must be included in all folders to signify they are a package/subpackage.


