""" dts.py

This module contains utility classes for dts testing. They are used
primarily in the dash app and the 

Classes:
    DtsTestType(str, Enum) - Enum containing test types RPM and TORQUE
    DtsCommand() - Container for dts motor commands
    DtsTestProfile() - Class used to configure dts test profile
"""

import enum
import json
import logging
import os

from pandas import DataFrame


class DtsTestType(str, enum.Enum):
    """ Enum containing the test types """
    
    RPM = "RPM"
    TORQUE = "TORQUE"
    
    
class DtsCommand():
    """ Container class for dts motor commands
    
    Attributes:
        type(DtsTestType) - Type of the dts command
        step(int) - The step duration of the command in ms
        value(int) - The value of the 
    
    """
    
    def __init__(self, cmdType: DtsTestType, step: int, value: int):
        self.type = cmdType
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
        testType(:obj: DtsTestType) - type of the test profile (RPM or TORQUE)
        commands(list of :obj: DtsCommand) - list of commands to send to the motor  

    Methods:
        exportJson() - exports this profile to JSON 
        getDf() - returns a commands dataframe
        
    """
    
    def __init__(self, name: str, testType:DtsTestType=DtsTestType.RPM, commands:list=[]):
        self.name = name
        self.testType = testType
        self.commands = commands
        
    def addCommand(self, command: DtsCommand):
        """ Adds a command """
        if type(command) != DtsCommand:
            raise TypeError("COMMAND TYPE HAS TO BE DTS COMMAND")
        else:
            self.commands.append(command)
        
    def clearLast(self):
        """ Removes the last (most recently added) command"""
        try:
            command = self.commands.pop(-1)
        except IndexError:
            logger = logging.getLogger("DTS-DASH")
            logger.info("COMMAND LIST EMPTY - NO COMMANDS REMOVED")
            return None
            
        return command
        
    def clearAll(self):
        self.commands = []

    def refresh(self):
        """ Restore the profile to the default values """
        self.name = None
        self.testType = DtsTestType.RPM
        self.commands = []
        
    def exportJson(self, folderPath:str=None):
        """ Export the profile to a json file in the specified folder
        
        Args:
            folderPath(str): Folder to place profiles.json in
                default - cwd
        """
        logger = logging.getLogger("DTS-DASH")
        if folderPath is None:
            folderPath = os.getcwd()
        
        pathToFile = os.path.join(folderPath, "profiles.json")
        
        # If folder DNE, create it
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        
        # If file DNE, create and initialize it
        if not os.path.isfile(pathToFile):
            initialDict = {
                "profiles": []
            }
            with open(pathToFile, 'w') as profileJson:
                json.dump(initialDict, profileJson, indent=4)
        
        with open(pathToFile, "r") as profileJson:
            current_profiles = json.load(profileJson)['profiles']
        
        with open(pathToFile, 'w') as profileJson:
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
    
    def getDf(self):
        """ Return a dataframe built from DTS Commands """
        return DataFrame([cmd.to_dict() for cmd in self.commands])
        
    def to_dict(self):
        """ Return a dict representation of the test profile """
        profile_dict = {
            "name": self.name,
            "type": self.testType,
            "commands": [command.to_dict() for command in self.commands]
        }
        return profile_dict
        
   