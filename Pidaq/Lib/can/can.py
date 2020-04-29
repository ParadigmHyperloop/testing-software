"""
"""
import json

import can

class CanManager:
    """
    """

    def __init__(self, bus_name: str) -> None:
        """
        """

        self.bus = can.interfaces.socketcan.SocketcanBus(channel=bus_name)
        self.messages = []
        self.message_ids =[]

    def read_message_config(self, project: str) -> None:
        if project.lower not in ["dts", "suspension", "windtunnel"]:
            raise Exception(f'Error: {project} is not a valid project')
        with open('messageconfig.json', 'r+') as config:
            config_dict = json.load(config)
            for reading in config_dict[project]['Readings']:
                self.messages.append(CanMessage(
                    project,
                    reading['MsgID'],
                    reading['Reading'],
                    reading['ConversionFactor'],
                    reading['ConversionFactorType']
                ))
                self.message_ids.append(reading['MsgID'])

    def read_bus(self) -> can.Message:
        message = self.bus.recv()
        return message

    def assign_message_data(self, bus_message: can.Message) -> None:
        message_id = bus_message.arbitration_id
        if message_id in self.message_ids:
            for message in self.messages:
                if message.message_id == bus_message.arbitration_id:
                    message.data = bus_message.data

class CanMessage:
    """
    """

    def __init__(self, project: str, message_id: str, reading: str, 
                 conversion_factor: str, conversion_factor_type: str) -> None:
        """
        """

        self.message_id = int(message_id, 16)
        self.reading = reading
        self.conversion_factor = parse_conversion_factor(conversion_factor, conversion_factor_type)
        self.data = None


def parse_conversion_factor(conversion_factor: str, conversion_factor_type: str):
    if conversion_factor_type.lower is 'float':
        return float(conversion_factor)
    elif conversion_factor_type.lower is 'int':
        return int(conversion_factor)
    else:
        return -1


if __name__ == "__main__":
    pass
