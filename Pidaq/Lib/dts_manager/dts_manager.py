

from can_manager import can_manager


class DTSManager:

    def __init__(self, bus_name: str):
        self.bus = can_manager.CanManager(bus_name)

    def configure_motor(self, configuration: dict) -> None:
        # Extract commands from dict
        self.torque_command = int(configuration['torque']).to_bytes(2, 'big')
        self.speed_command = int(configuration['speed']).to_bytes(2, 'big')
        self.direction_command = int(
            configuration['direction']).to_bytes(1, 'big')
        self.inverter_enable = int(configuration['inverterEnable'])
        self.inverter_discharge = int(configuration['inverterDischarge'])
        self.speed_mode_enable = int(configuration['speedModeEnable'])
        self.mode = ((int(self.speed_mode_enable) << 2) +
                     (int(self.inverter_discharge) << 1) + (int(self.inverter_enable) << 0)).to_bytes(1, 'big')
        self.commanded_torque_limit = int(
            configuration['commandedTorqueLimit']).to_bytes(2, 'big')

    def send_motor_command(self) -> None:
        command_list = bytes(self.torque_command, self.speed_command,
                             self.direction_command, self.mode, self.commanded_torque_limit)
        self.bus.send_message(192, command_list)

    def convert_temperatures(self) -> None:
        module_a_temperature = int.from_bytes(self.bus.messages['0x0A0'].data[1] +
                                              self.bus.messages['0x0A0'].data[0], byteorder='big')
