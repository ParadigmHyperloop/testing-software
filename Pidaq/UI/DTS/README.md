# DTS Control and Data Visualization GUI
This directory contains all user interface code for the Dynamic Test Stand, including the dash application and grafana dashboard.

## Overview
The folder consists of the following components:
* `grafana` - Contains grafana configuration for DTS data vis. dashboard
* `dts-dash.py` - Entrypoint of the dash application, imports all of the layout and callback code defined elsewhere
* `dts_dash` - Python package containing the layout and callback subpackages, and the dash app declaration
    * `assets` - Bootstrap css and custom css for adding some (very) basic styling to the dash layouts
    * `callbacks` - Contains callbacks for both the control and sensor tabs
    * `layout` - Contains dash layouts for control and sensor tabs
    * `app.py` - Dash app initialization, imported by callbacks. Need this defined here to avoid circular imports

## Setup
To run the dash app, python and the required packages (as seen in requirements.txt at the root of the repo) must be installed.
It is recommended to use a virtual env for this. Setup instructions for python and venv can be found here: <https://sites.google.com/mun.ca/testing-software-wiki/guides/python-env>

## Usage
To launch the dts dashboard, simply navigate to the DTS folder (ensure you are in the correct python env) and type:
```
python3 dts-dash.py 
```
Alternatively, you can use your debugger to launch the file. After launching the script, go to: <http://127.0.0.1:8050/> to view the dashboard.


