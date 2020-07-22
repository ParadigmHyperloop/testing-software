"""Contains classes and methods to implement and manage the can (socketcan) bus

Classes:
    CanManager
    SensorReading

Functions:
    parse_conversion_factor
"""
import json
import os

import can


class CanManager:
    """Manages the can bus, and sets the SensorReading objects for the test being run

    This class contains the socketcan bus instance that will be used to communicate with
    the sensor board, as well as the configured sensor readings for the particular project
    that is being tested

    Attributes:
        bus (can.interfaces.socketcan.SocketcanBus)
        messages (dict): dict of all the messages to be expected from the
                         sensor board. Keys are message ids, and values are
                         SensorReading objects

    Methods:
        read_message_config(project: str)
            Reads the configuration of sensor readings from messageconfig.json
        send_message(id: int, data: list)
        read_bus
            Reads the bus for a message
        assign_message_data(bus_message: can.Message)
            assigns data to the correct SensorReading object
    """

    def __init__(self, bus_name: str, message_frequency: float) -> None:
        self.bus = can.interfaces.socketcan.SocketcanBus(channel=bus_name)
        self.messages = {}
        self.message_frequency = message_frequency

    def read_message_config(self, project: str, config_file: str, path=None) -> None:
        """Reads sensor readings configuration from messageconfig.json

        Constructs SensorReading objects for all expected sensor readings,
        and appends them to a list

        Parameters:
            project (str): current project, must be one of dts, suspension, or windtunnel
            config_file (str): message configuration file name
            path (str): path to folder containing configuration file, if no path specified, current working
                        directory is assumed
        """
        if project.lower() not in ["dts", "suspension", "windtunnel"]:
            raise ValueError(f'Error: {project} is not a valid project')
        file_path = os.getcwd() if path is None else path
        with open(os.path.join(file_path, config_file), 'r+') as config:
            config_dict = json.load(config)
            for reading in config_dict[project.lower()]['readings']:
                message_id = reading['message_id']
                self.messages[message_id] = SensorReading(
                    reading['message_id'],
                    reading['reading'],
                    reading['conversion_factor'] if reading['conversion_factor'] else None,
                )

    def send_message(self, id: int, data: list) -> None:
        if id in self.messages.keys():
            raise Exception(f'Error: ID: {id} is already in use')
        message = can.Message(arbitration_id=id, data=data)
        self.bus.send(message)

    def send_message_periodic(self, message: can.Message, duration: float):
        if message.arbitration_id in self.messages.keys():
            raise Exception(f'Error: ID: {id} is already in use')
        return self.bus.send_periodic(message, self.message_frequency, duration=duration)

    def read_bus(self, timeout_seconds=None) -> can.Message:
        message = self.bus.recv(timeout_seconds)
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
        if message_id in self.messages.keys():
            self.messages[message_id].data = bus_message.data


class SensorReading:
    """Class used to store information about sensor readings to be received on can bus

    This class contains all the information about the project-specific sensor measurement
    readings that will be sent over the can bus from the sensor board to the raspberry pi

    Attributes:
        message_id (int): represents the can arbitration id, is a hexidecimal integer
        reading (str): contains the name of the measurement
        conversion_factor: contains the conversion factor for the reading,
                            or a dict of factors if there are multiple
        data (int or float)
    """

    def __init__(self, message_id: str, reading: str,
                 conversion_factor) -> None:
        self.message_id = message_id
        self.reading = reading
        self.conversion_factor = conversion_factor
        self.data = None


if __name__ == "__main__":
    """Note: To send messages in test case, must be running linux to make use of socketcan

    This test case makes use of the canSender program, see README for instructions
    """
    bus = CanManager('vcan0')
    bus.read_message_config('dts', 'example_message_config.json')

    # Print SensorReading objects
    for id, message in bus.messages.items():
        print(
            f'Message id: {message.message_id}    Reading: {message.reading}    Conversion Factor: {message.conversion_factor}')

    # Print contents of method_ids list
    print('Message ids in use:')
    for message_id in bus.messages.keys():
        print(message_id)

    # Start receiving messages and assigning message data
    while True:
        current_message = bus.read_bus()
        bus.assign_message_data(current_message)
        for id, message in bus.messages.items():
            print(f'Reading: {message.reading}   data: {message.data}')

        # Send a control message, check the can_reciever program output for this message
        bus.send_message(55, bytes('control', 'utf-8'))
