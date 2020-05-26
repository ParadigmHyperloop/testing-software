from can_manager import can_manager


class DTSManager:

    def __init__(self, bus_name: str):
        self.bus = can_manager.CanManager(bus_name)
        self.module_a_temperature = None
        self.module_b_temperature = None
        self.module_c_temperature = None
        self.gate_driver_board_temperature = None
        self.control_board_temperature = None
        self.rtd_1_temperature = None
        self.rtd_2_temperature = None
        self.rtd_3_temperature = None
        self.rtd_4_temperature = None
        self.rtd_5_temperature = None

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
        command_list = self.torque_command + self.speed_command + \
            self.direction_command + self.mode + self.commanded_torque_limit
        self.bus.send_message(192, command_list)

    def convert_temperatures(self) -> None:
        if self.bus.messages['0xa0'].data and self.bus.messages['0xa1'].data and self.bus.messages['0xa2'].data:
            print(self.bus.messages['0xa0'].data[1])
            self.module_a_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[2:0:-1], byteorder='big') / 10
            self.module_b_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[4:2:-1], byteorder='big') / 10
            self.module_c_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[6:4:-1], byteorder='big') / 10
            self.gate_driver_board_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[:6:-1], byteorder='big') / 10
            self.control_board_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[2:0:-1], byteorder='big') / 10
            self.rtd_1_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[4:2:-1], byteorder='big') / 10
            self.rtd_2_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[6:4:-1], byteorder='big') / 10
            self.rtd_3_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[:6:-1], byteorder='big') / 10
            self.rtd_4_temperature = int.from_bytes(
                self.bus.messages['0xa2'].data[2:0:-1], byteorder='big') / 10
            self.rtd_5_temperature = int.from_bytes(
                self.bus.messages['0xa2'].data[4:2:-1], byteorder='big') / 10

    def convert_torques(self) -> None:
        pass


if __name__ == "__main__":
    import can
    dts = DTSManager('vcan0')
    dts.bus.read_message_config('dts', 'message_config.json')

    motorConfiguration = {
        'torque': 2000,
        'speed': 0,
        'direction': 90,
        'inverterEnable': 1,
        'inverterDischarge': 0,
        'speedModeEnable': 0,
        'commandedTorqueLimit': 5000
    }

    dts.configure_motor(motorConfiguration)
    while True:
        dts.send_motor_command()
        current_message = dts.bus.read_bus()
        dts.bus.assign_message_data(current_message)
        dts.convert_temperatures()
        print(dts.module_a_temperature)
        print(dts.module_b_temperature)
