

from can_manager import can_manager


class DTSManager:

    def __init__(self, bus_name: str):
        self.bus = can_manager.CanManager(bus_name)

    def configure_motor(self, configuration: dict) -> None:
        # Extract commands from dict
        torque_command = int(configuration['torque']).to_bytes(2, 'big')
        speed_command = int(configuration['speed']).to_bytes(2, 'big')
        direction_command = int(configuration['direction']).to_bytes(1, 'big')
        inverter_enable = int(configuration['inverterEnable'])
        inverter_discharge = int(configuration['inverterDischarge'])
        speed_mode_enable = int(configuration['speedModeEnable'])
        mode = ((int(speed_mode_enable) << 2) +
                (int(inverter_discharge) << 1) + (int(inverter_enable) << 0)).to_bytes(1, 'big')
        commanded_torque_limit = int(
            configuration['commandedTorqueLimit']).to_bytes(2, 'big')

        # Create 8 Byte message
        command_list = bytes(torque_command, speed_command,
                             direction_command, mode, commanded_torque_limit)
        self.bus.send_message(192, command_list)
