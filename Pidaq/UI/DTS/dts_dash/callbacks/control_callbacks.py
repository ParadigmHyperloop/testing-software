import json
import logging
import os

import dash
from dash.dependencies import Input, Output, State
from dash.dash import no_update 

from dts_dash.app import app
from dts_dash.layout.control import control_layout
from paralogging import logInit
from utils.dts import DtsTestProfile, DtsCommand, DtsTestType

# Configure root logger
logger = logging.getLogger()
logInit.log_init('DTS', logger, logLevel="WARNING")
logger.info("ROOT LOGGER INITIALIZED")

logger = logging.getLogger("DTS-DASH")
logger.setLevel("INFO")

# Restrict werkzeug logger to warning level
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel("WARNING")

# Instantiate test profile 
test_profile = DtsTestProfile(None)


# Toggle confirmation dialogue modal
@app.callback(
    Output("start-confirm-dialog", "is_open"),
    [Input("submit-start-btn", "n_clicks"), 
     Input("abort-start-btn", "n_clicks" ),
     Input("test-start-btn", "n_clicks")],
    [State("start-confirm-dialog", "is_open")]
)
def toggle_start_modal(submit, abort, start, is_open):
    if submit or abort or start:
        return not is_open
    return is_open


# Fired when accepting the confirmation modal - TEST START 
@app.callback(
    Output("dump-start-clicked", "children"),
    [Input("submit-start-btn", "n_clicks")]
)
def submit(nstarts):
    if not nstarts:
        raise dash.exceptions.PreventUpdate
    
    logger.warn(f"SUBMIT CLICKED - {nstarts} TIMES")
    return ""


# Fired when abort start is clicked
@app.callback(
    Output("dump-abort-start", "children"),
    [Input("abort-start-btn", "n_clicks")]
)
def abort(n_aborts):
    if not n_aborts:
         raise dash.exceptions.PreventUpdate
     
    logger.warn("START ABORTED")
   
   
# Update title callback
@app.callback(
    Output("test-title-header", "children"),
    [Input("update-title-btn", "n_clicks")],
    [State("test-title-input", "value")]
)
def update_title(n_clicks, title):
    global test_profile
    
    # This prevents dash from firing the callback on page load. 
    if not n_clicks:
        # Clear the previous profile 
        test_profile.refresh()
        raise dash.exceptions.PreventUpdate
        
    test_profile.name = title
    logger.info(f"UPDATED PROFILE NAME TO: {test_profile.name}")
    
    return title


# Fired by any button that changes the timestep readout, updates table
@app.callback(
    [Output("timestep-readout-tbl", "children"),
    Output("rpm-torque-display", "children")],
    [Input("add-command-btn", "n_clicks"),
     Input("clear-last-btn", "n_clicks"),
     Input("clear-all-btn", "n_clicks"),
     Input("rpm-toggle-btn", "n_clicks"),
     Input("torque-toggle-btn", "n_clicks")],
    [State("rpm-torque-value", "value"),
     State("step-duration-input", "value")]
)
def update_commands(add_cmd_clicks, last_clicks, all_clicks, rpm_clicks, torque_clicks, value, step):
    
    # If none of the buttons that update the commands are clicked, prevent update
    clicks = [add_cmd_clicks, last_clicks, all_clicks, rpm_clicks, torque_clicks]
    if not sum([click if click is not None else 0 for click in clicks]):
        raise dash.exceptions.PreventUpdate
    
    # Use global test profile
    global test_profile
    ret_value = test_profile.get_table_data(), no_update

    ctx = dash.callback_context
    
    # Get the id of the most recently triggered button
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == "add-command-btn":
        # Cancel adding command if name is none
        if test_profile.name is None:
            raise dash.exceptions.PreventUpdate
        
        # Cancel adding the command if the value is None
        if value is None or step is None:
            raise dash.exceptions.PreventUpdate
        
        test_type = test_profile.test_type
        command = DtsCommand(test_type, step, value)
        test_profile.add_command(command)
    
        logger.info(f"COMMAND ADDED: {test_profile.commands[-1]}")
        ret_value = test_profile.get_table_data(), no_update
        
    elif button_id == "clear-all-btn":
        test_profile.clear_all()
        ret_value = test_profile.get_table_data(), no_update
        logger.info(f"CLEAR ALL PRESSED - CLEARED ALL COMMANDS")
    
    elif button_id == "clear-last-btn":
        removed_cmd = test_profile.clear_last()
        ret_value = test_profile.get_table_data(), no_update
        logger.info(f"CLEAR LAST PRESSED - REMOVED COMMAND: {removed_cmd}")
   
    elif button_id == "rpm-toggle-btn":
        if test_profile.test_type != DtsTestType.RPM:
            test_profile.test_type = DtsTestType.RPM
            test_profile.commands = []
            logger.info(f"RPM TOGGLED, PROFILE " 
                        f"IS NOW OF TYPE: {test_profile.test_type}")
            
            ret_value = test_profile.get_table_data(), "RPM"
            
        else:
            logging.info("RPM TOGGLED - TEST TYPE IS ALREADY RPM " 
                         "- NO ACTION TAKEN ")
            raise dash.exceptions.PreventUpdate
        
    elif button_id == "torque-toggle-btn":
        if test_profile.test_type != DtsTestType.TORQUE:
            test_profile.test_type = DtsTestType.TORQUE
            test_profile.commands = []
            logger.info(f"TORQUE TOGGLED, PROFILE " 
                        f"IS NOW OF TYPE: {test_profile.test_type}")
            
            ret_value = test_profile.get_table_data(), "TOR"
        
        else:
            logging.info("TORQUE TOGGLED - TEST TYPE IS ALREADY TORQUE " 
                         "- NO ACTION TAKEN ")
            raise dash.exceptions.PreventUpdate
            
    return ret_value


# Fired when adding a command, raises required alerts
@app.callback(
    [Output("exceed-60s-alert", "is_open"),
    Output("no-name-alert", "is_open"),
    Output("invalid-value-alert", "is_open")],
    [Input("add-command-btn", "n_clicks")],
    [State("rpm-torque-value", "value"),
     State("step-duration-input", "value")]
)
def error_on_add_command(add_cmd_clicks, value, step):
    
    # If none of the buttons that update the commands are clicked, prevent update
    if not add_cmd_clicks: 
        raise dash.exceptions.PreventUpdate
    
    # Use global test profile
    global test_profile
    
    # Perform checks for various warnings
    if test_profile.name is None:
        logger.warning("NO NAME SELECTED - "
                       "PLEASE SELECT A PROFILE NAME BEFORE ADDING COMMANDS") 
        return no_update, True, no_update   
    
    if value is None or step is None:
        logger.warning("TRIED TO ADD A COMMAND WITH NO TIMESTEP OR NO VALUE")
        return no_update, no_update, True
    
    # Check if total test time exceeds 60s
    current_test_time = sum([command.step for command in test_profile.commands])
    new_total_test_time = step + current_test_time
    
    if new_total_test_time > 60000:
        logger.warn(f"TOTAL TEST TIME OF {new_total_test_time}ms " 
                    "/ {new_total_test_time/1000}s EXCEEDS 1 MINUTE")
        return True, no_update, no_update
    else:
        return no_update, no_update, no_update
            
    
@app.callback(
Output("dump-export-profile", "children"),
[Input("export-profile-btn", "n_clicks")]
)
def export_profile(n_clicks):
    if not n_clicks:
        raise dash.exceptions.PreventUpdate
        
    global test_profile
    test_profile.export_json()
    return ""
