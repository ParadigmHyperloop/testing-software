"""Contains classes and methods to implement and manage the can (socketcan) bus

Classes:
    CanManager
    SensorReading

Functions:
    parse_conversion_factor
"""
import json

import can


class CanManager:
    """Manages the can bus, and sets the SensorReading objects for the test being run

    This class contains the socketcan bus instance that will be used to communicate with
    the sensor board, as well as the configured sensor readings for the particular project
    that is being tested

    Attributes:
        bus (can.interfaces.socketcan.SocketcanBus)
        messages (list(SensorReading)): list of all the messages to be expected from the 
                                        sensor board
        message_ids (list(int)): list of all the message ids, hexidecimal integers

    Methods:
        read_message_config(project: str)
            Reads the configuration of sensor readings from messageconfig.json
        send_message(id: int, data: list)
        read_bus
            Reads the bus for a message
        assign_message_data(bus_message: can.Message)
            assigns data to the correct SensorReading object
    """

    def __init__(self, bus_name: str) -> None:
        self.bus = can.interfaces.socketcan.SocketcanBus(channel=bus_name)
        self.messages = []
        self.message_ids = []

    def read_message_config(self, project: str) -> None:
        """Reads sensor readings configuration from messageconfig.json

        Constructs SensorReading objects for all expected sensor readings,
        and appends them to a list

        Parameters:
            project(str): current project, must be one of dts, suspension, or windtunnel
        """

        if project.lower not in ["dts", "suspension", "windtunnel"]:
            raise Exception(f'Error: {project} is not a valid project')
        with open('messageconfig.json', 'r+') as config:
            config_dict = json.load(config)
            for reading in config_dict[project]['Readings']:
                self.messages.append(SensorReading(
                    project,
                    reading['MsgID'],
                    reading['Reading'],
                    reading['ConversionFactor'],
                    reading['ConversionFactorType']
                ))
                self.message_ids.append(int(reading['MsgID'], 16))

    def send_message(self, id: int, data: list) -> None:
        if id in self.message_ids:
            raise Exception(f'Error: ID: {id} is already in use')
        message = can.Message(arbitration_id=id, data=data)
        self.bus.send(message)

    def read_bus(self) -> can.Message:
        message = self.bus.recv()
        return message

    def assign_message_data(self, bus_message: can.Message) -> None:
        """Assigns message data to the correct SensorReading object

        Assigns message data to the correct SensorReading object
        based on the arbitration_id of the message, checks to ensure
        that arbitration_id is in list of ids for the test

        Parameters:
            bus_message(can.Message)
        """
        message_id = bus_message.arbitration_id
        if message_id in self.message_ids:
            for message in self.messages:
                if message.message_id == bus_message.arbitration_id:
                    message.data = bus_message.data


class SensorReading:
    """Class used to store information about sensor readings to be received on can bus

    This class contains all the information about the project-specific sensor measurement
    readings that will be sent over the can bus from the sensor board to the raspberry pi

    Attributes:
        message_id (int): represents the can arbitration id, is a hexidecimal integer
        reading (str): contains the name of the measurement
        conversion_factor (int or float)
        conversion_factor_type (str)
        data (int or float)

    Methods:

    """

    def __init__(self, project: str, message_id: str, reading: str,
                 conversion_factor: str, conversion_factor_type: str) -> None:
        self.message_id = int(message_id, 16)
        self.reading = reading
        self.conversion_factor = parse_conversion_factor(
            conversion_factor, conversion_factor_type)
        self.data = None


def parse_conversion_factor(conversion_factor: str, conversion_factor_type: str):
    """Converts a string conversion factor into the correct numerical representation

    Given the string representation of a conversion factor, as well as its type,
    this function returns the conversion factor in its correct numerical representation,
    either int or float

    Parameters:
        conversion_factor(str)
        conversion_factor_type(str)

    Returns:
        conversion_factor(int or float)
    """
    if conversion_factor_type.lower is 'float':
        return float(conversion_factor)
    elif conversion_factor_type.lower is 'int':
        return int(conversion_factor)
    else:
        return -1


if __name__ == "__main__":
    pass
