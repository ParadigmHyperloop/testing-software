# Stability dash entrypoint
import time

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State

import stability_dash.callbacks.control_callbacks
from stability_dash.app import app
from stability_dash.layout.control import control_layout

app.layout = control_layout

if __name__ == "__main__":
    app.run_server(debug=False)
