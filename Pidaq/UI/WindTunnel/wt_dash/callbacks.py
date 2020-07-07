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
logInit.log_init('DTS', logger, logLevel="WARNING")
logger.info("ROOT LOGGER INITIALIZED")
