import logging

import dash
from dash.dependencies import Input, Output, State

from dts_dash.app import app
from dts_dash.layout.control import control_layout

logger = logging.getLogger("DTS-LOGGER")

@app.callback(
    Output("start-confirm-dialog", "is_open"),
    [Input("submit-start", "n_clicks"), 
     Input("abort-start", "n_clicks" ),
     Input("test-start", "n_clicks")],
    [State("start-confirm-dialog", "is_open")]
)
def toggle_start_modal(submit, abort, start, is_open):
    if submit or abort or start:
        return not is_open
    return is_open
    
# This where the start modal gets fired
@app.callback(
    Output("test-title", "children"),
    [Input("submit-start", "n_clicks")]
)
def submit(nstarts):
    if not nstarts:
        raise dash.exceptions.PreventUpdate
    return f"Submit clicked: {nstarts} times"
    
@app.callback(
    Output("dump", "children"),
    [Input("abort-start", "n_clicks")]
)
def submit(n_aborts):
    logger.warn("START ABORTED")
   
