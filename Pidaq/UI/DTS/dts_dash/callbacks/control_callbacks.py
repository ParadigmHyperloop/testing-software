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
    # This prevents dash from firing the callback on page load. 
    global test_profile
    
    if not n_clicks:
        # Clear the previous profile 
        test_profile.refresh()
        raise dash.exceptions.PreventUpdate
        
    test_profile.name = title
    logger.info(f"Title read: {title}, updated profile name: {test_profile.name}")
    
    return title

# TODO refactor to move alerts to their own callbacks
# This way, this function need not return 80000 no updates
# Fired by any button that changes the timestep readout
@app.callback(
    [Output("timestep-readout-tbl", "children"),
    Output("rpm-torque-display", "children"),
    Output("exceed-60s-alert", "is_open"),
    Output("no-name-alert", "is_open"),
    Output("invalid-value-alert", "is_open")],
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
    if not add_cmd_clicks and not last_clicks and not all_clicks and not rpm_clicks and not torque_clicks:
        raise dash.exceptions.PreventUpdate
    
    # Use global test profile
    global test_profile
    ret_value = test_profile.get_table_data(), no_update, no_update, no_update, no_update
    
    ctx = dash.callback_context
    
    # Get the id of the most recently triggered button
    if not ctx.triggered:
        button_id = 'RPM/TORQUE Toggles not clicked yet'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # TODO Not allow adding a value of its invalid
    if button_id == "add-command-btn":
        # Cancel adding the command if the value is None
        if value is None or step is None:
            logger.warning("TRIED TO ADD A COMMAND WITH NO TIMESTEP OR NO VALUE")
            ret_value = ret_value = no_update, no_update, no_update, no_update, True
            return ret_value
        
        # Cancel adding command if name, step, or value is None - display warning
        if test_profile.name is None:
            logger.warning("NO NAME SELECTED - PLEASE SELECT A PROFILE NAME BEFORE ADDING COMMANDS") 
            ret_value = no_update, no_update, no_update, True, no_update
            return ret_value
            
        # Warn if new command makes test length > 60 secs (60 000ms)
        current_test_time = sum([command.step for command in test_profile.commands])
        new_total_test_time = step + current_test_time
        
        if new_total_test_time > 60000:
            logger.warn(f"TOTAL TEST TIME OF {new_total_test_time}ms / {new_total_test_time/1000}s EXCEEDS 1 MINUTE")
            toggle_time_warning = True
        else:
            toggle_time_warning = False
            
        test_type = test_profile.test_type
        command = DtsCommand(test_type, step, value)
        test_profile.add_command(command)
    
        logger.info(f"COMMAND ADDED: {test_profile.commands[-1]}")
        ret_value = test_profile.get_table_data(), no_update, toggle_time_warning, no_update, no_update
        
    elif button_id == "clear-all-btn":
        test_profile.clear_all()
        ret_value = test_profile.get_table_data(), no_update, no_update, no_update, no_update
        logger.info(f"CLEAR ALL PRESSED - CLEARED ALL COMMANDS")
    
    elif button_id == "clear-last-btn":
        removed_cmd = test_profile.clear_last()
        ret_value = test_profile.get_table_data(), no_update, no_update, no_update, no_update
        logger.info(f"CLEAR LAST PRESSED - REMOVED COMMAND: {removed_cmd}")
   
    elif button_id == "rpm-toggle-btn":
        # If test type wasnt rpm, update test profile to rpm and clear commands 
        if test_profile.test_type != DtsTestType.RPM:
            test_profile.test_type = DtsTestType.RPM
            test_profile.commands = []
            logger.info(f"Test type updated to RPM, updated " 
                        f"profile test type to: {test_profile.test_type}")
            
            ret_value = test_profile.get_table_data(), "RPM", no_update, no_update, no_update
            
        # If test profile type is already rpm - do nothing
        else:
            logging.info("RPM TOGGLE CLICKED - TEST TYPE IS ALREADY RPM - NO ACTION TAKEN ")
            raise dash.exceptions.PreventUpdate
        
    elif button_id == "torque-toggle-btn":
        # If test type wasnt torque, update test profile to torque and clear commands 
        if test_profile.test_type != DtsTestType.TORQUE:
            test_profile.test_type = DtsTestType.TORQUE
            test_profile.commands = []
            logger.info(f"Test type updated to torque, updated " 
                        f"profile test type to: {test_profile.test_type}")
            
            ret_value = test_profile.get_table_data(), "TOR", no_update, no_update, no_update
        
        else:
            logging.info("TORQUE TOGGLE CLICKED - TEST TYPE IS ALREADY TORQUE - NO ACTION TAKEN ")
            raise dash.exceptions.PreventUpdate
            
    return ret_value


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
