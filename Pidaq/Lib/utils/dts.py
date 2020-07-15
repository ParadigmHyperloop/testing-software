""" dts.py

This module contains utility classes for dts testing. They are used
primarily in the dash app.

Classes:
    DtsTestType(str, Enum) - Enum containing test types RPM and TORQUE
    DtsCommand() - Container for dts motor commands
    DtsTestProfile() - Class used to configure dts test profile
"""

import json
import logging
import os
from enum import Enum

import dash_bootstrap_components as dbc
import dash_html_components as html
from pandas import DataFrame


class DtsTestType(str, Enum):
    """ Enum containing the DTS test types """
    
    RPM = "RPM"
    TORQUE = "TORQUE"
    
    
class DtsCommand():
    """ Container class for dts motor commands
    
    Attributes:
        type(DtsTestType) - Type of the dts command
        step(int) - The step duration of the command in ms
        value(int) - The value of the 
    
    """
    
    def __init__(self, cmd_type: DtsTestType, step: int, value: int):
        self.type = cmd_type
        self.step = step
        self.value = value
    
    def to_dict(self) -> dict:
        """ Convert dts command object to a dict """
        return {
            "Type": self.type,
            "Step Duration(ms)": self.step,
            "Value": self.value
        }
     
    def __str__(self):
        return f"TYPE: {self.type} | STEP DURATION(ms): {self.step} | VALUE: {self.value}"
    

class DtsTestProfile():
    """ Class representing a DTS test profile 
    
    Attributes: 
        name(str) - test profile name
        test_type(DtsTestType) - type of the test profile (RPM or TORQUE)
        commands(list of :obj: DtsCommand) - list of commands to send to the motor  

    Methods:
        add_command(command) - appends a command to the profile 
        clear_last() - removes the most recently added command 
        clear_all() - clears all commands 
        refresh() - restores the profile to default values
        export_json(filepath) - exports profile to a JSON 
        get_df() - returns the list of commands in a dataframe
        to_dict() - returns a dict representation of the test profile
    """
    
    def __init__(self, name: str, test_type: DtsTestType=DtsTestType.RPM, commands: list=[]):
        self.name = name
        self.test_type = test_type
        self.commands = commands
        
    def add_command(self, command: DtsCommand):
        """ Adds a command """
        if type(command) != DtsCommand:
            raise TypeError("COMMAND TYPE HAS TO BE DTS COMMAND")
        else:
            self.commands.append(command)
        
    def clear_last(self):
        """ Removes the last (most recently added) command"""
        try:
            command = self.commands.pop(-1)
        except IndexError:
            logger = logging.getLogger("DTS-DASH")
            logger.info("COMMAND LIST EMPTY - NO COMMANDS REMOVED")
            return None
            
        return command
        
    def clear_all(self):
        """ Removes all commands from the profile """
        self.commands = []

    def refresh(self):
        """ Restore the profile to the default values """
        self.name = None
        self.test_type = DtsTestType.RPM
        self.commands = []
        
    def export_json(self, folder_path: str=None):
        """ Export the profile to a json file in the specified folder
        
        Args:
            folder_path(str): Folder to place profiles.json in
                default - cwd
        """
        logger = logging.getLogger("DTS-DASH")
        if folder_path is None:
            folder_path = os.getcwd()
        
        path_to_file = os.path.join(folder_path, "profiles.json")
        
        # If folder DNE, create it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        # If file DNE, create and initialize it
        if not os.path.isfile(path_to_file):
            initialDict = {
                "profiles": []
            }
            with open(path_to_file, 'w') as profileJson:
                json.dump(initialDict, profileJson, indent=4)
        
        with open(path_to_file, "r") as profileJson:
            current_profiles = json.load(profileJson)['profiles']
        
        with open(path_to_file, 'w') as profileJson:
            
            # Update profile if it already exists, otherwise create a new one
            for profile in current_profiles:
                if profile['name'] == self.name:
                    profile.update(self.to_dict())
                    logger.info(f"UPDATED PROFILE - {self.name}")
                    break
            else:
                current_profiles.append(self.to_dict())
                logger.info(f"ADDED PROFILE - {self.name}")
                
            json.dump({"profiles": current_profiles}, profileJson)
        
        return 0
    
    def get_df(self):
        """ Return a dataframe built from DTS Commands """
        return DataFrame([cmd.to_dict() for cmd in self.commands])
        
    def to_dict(self):
        """ Return a dict representation of the test profile """
        profile_dict = {
            "name": self.name,
            "type": self.test_type,
            "commands": [command.to_dict() for command in self.commands]
        }
        return profile_dict
        
    def get_table_data(self):
        """ Return bootstrap table representation of this profile """
        table_header = [
            html.Thead(html.Tr([html.Th("Type"), 
                                html.Th("Step Duration(ms)"), 
                                html.Th("Value")]))
        ]

        table_rows = []
        
        for cmd in self.commands:
            row = html.Tr([
                html.Td(cmd.type), html.Td(cmd.step), html.Td(cmd.value)
            ])
            table_rows.append(row)
            
        table_body = [html.Tbody(table_rows)]
        
        return table_header + table_body
        