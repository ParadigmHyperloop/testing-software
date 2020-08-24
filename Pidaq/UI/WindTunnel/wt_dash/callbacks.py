""" callbacks.py 

Contains callbacks for the WindTunnel dash application
"""
import logging
import os

import dash
from dash.dependencies import Input, Output, State
from dash.dash import no_update 

from wt_dash.app import app
from wt_dash.layout import control_gui
from paralogging import logInit

# Configure root logger
logger = logging.getLogger()
logInit.log_init('WindTunnel', logger, logLevel="WARNING")
logger.info("ROOT LOGGER INITIALIZED")

logger = logging.getLogger("WT-DASH")
logger.setLevel("INFO")

# Calculated values and constants dropdown
@app.callback(
    [Output("calculated-values-collapse", "is_open"),
     Output("collapse-constants-btn", "children")],
    [Input("collapse-constants-btn", "n_clicks")],
    [State("calculated-values-collapse", "is_open")],
)
def toggle_constants_collapse(n_clicks, is_open):
    if n_clicks:
        # If the Dropdown is open, close it and make the button show +
        if is_open:
            return False, "+"
        
        # If the dropdown is closed, open it and make the button show - 
        else:
            return True, "-" 

    return is_open, '+'

# Distance Sensor reading dropdown
@app.callback(
    [Output("distance-values-collapse", "is_open"),
     Output("distance-sensor-btn", "children")],
    [Input("distance-sensor-btn", "n_clicks")],
    [State("distance-values-collapse", "is_open")],
)
def toggle_distance_collapse(n_clicks, is_open):
    if n_clicks:
        # If the Dropdown is open, close it and make the button show +
        if is_open:
            return False, "+"
        
        # If the dropdown is closed, open it and make the button show - 
        else:
            return True, "-" 

    return is_open, '+'

