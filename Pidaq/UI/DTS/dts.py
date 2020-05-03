import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State

from dts_dash.app import app
from dts_dash.layout.control import control_layout
from dts_dash.layout.sensor import sensor_layout
from dts_dash.callbacks import control_callbacks, sensors_callbacks


tabs = dbc.Tabs(
    [
        # TODO - implement the control tab
        dbc.Tab(control_layout, label="Controls", tabClassName="hov-pointer"),
        
        # TODO - implement the sensor tab
        dbc.Tab(sensor_layout, label="Sensors", tabClassName="hov-pointer")  
    ] 
)

app.layout = tabs

if __name__ == "__main__":
    app.run_server(debug=False)