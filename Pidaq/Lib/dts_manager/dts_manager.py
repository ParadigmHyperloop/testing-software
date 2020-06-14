from can_manager import can_manager

class DTSControl():

    def __init__(self, bus: can_manager.CanManager):
        self.bus = bus

    def configure_motor(self, configuration: dict) -> None:
        # Extract commands from dict
        self.torque_command = int(
            configuration['torque']).to_bytes(2, 'little')
        self.speed_command = int(configuration['speed']).to_bytes(2, 'little')
        self.direction_command = int(
            configuration['direction']).to_bytes(1, 'little')
        self.inverter_enable = int(configuration['inverterEnable'])
        self.inverter_discharge = int(configuration['inverterDischarge'])
        self.speed_mode_enable = int(configuration['speedModeEnable'])
        self.mode = ((int(self.speed_mode_enable) << 2) +
                     (int(self.inverter_discharge) << 1) + (int(self.inverter_enable) << 0)).to_bytes(1, 'little')
        self.commanded_torque_limit = int(
            configuration['commandedTorqueLimit']).to_bytes(2, 'little')

    def send_motor_command(self) -> None:
        command_list = self.torque_command + self.speed_command + \
            self.direction_command + self.mode + self.commanded_torque_limit
        self.bus.send_message(192, command_list)


class DTSTelemetry():

    def __init__(self, bus: can_manager.CanManager):
        self.bus = bus
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
        self.analog_input_1 = None
        self.analog_input_2 = None
        self.analog_input_3 = None
        self.analog_input_4 = None
        self.dc_bus_voltage = None
        self.output_voltage = None
        self.vab_vd_voltage = None
        self.vbc_vq_voltage = None
        self.motor_angle = None
        self.delta_filter_resolved = None
        self.one_five_voltage_ref = None
        self.two_five_voltage_ref = None
        self.five_voltage_ref = None
        self.twelve_system_voltage = None
        self.digital_input_1 = None
        self.digital_input_2 = None
        self.digital_input_3 = None
        self.digital_input_4 = None
        self.digital_input_5 = None
        self.digital_input_6 = None
        self.digital_input_7 = None
        self.digital_input_8 = None
        self.id_feedback = None
        self.iq_feedback = None
        self.torque_shudder = None
        self.commanded_torque = None

    def convert_temperatures(self) -> None:
        if self.bus.messages['0xa0'].data:
            self.module_a_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[0:2], byteorder='little', signed=True) / 10
            self.module_b_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[2:4], byteorder='little', signed=True) / 10
            self.module_c_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[4:6], byteorder='little', signed=True) / 10
            self.gate_driver_board_temperature = int.from_bytes(
                self.bus.messages['0xa0'].data[6:], byteorder='little', signed=True) / 10
        if self.bus.messages['0xa1'].data:
            self.control_board_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[0:2], byteorder='little', signed=True) / 10
            self.rtd_1_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[2:4], byteorder='little', signed=True) / 10
            self.rtd_2_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[4:6], byteorder='little', signed=True) / 10
            self.rtd_3_temperature = int.from_bytes(
                self.bus.messages['0xa1'].data[6:], byteorder='little', signed=True) / 10
        if self.bus.messages['0xa2'].data:
            self.rtd_4_temperature = int.from_bytes(
                self.bus.messages['0xa2'].data[0:2], byteorder='little', signed=True) / 10
            self.rtd_5_temperature = int.from_bytes(
                self.bus.messages['0xa2'].data[2:4], byteorder='little', signed=True) / 10

    def convert_low_voltages(self) -> None:
        if self.bus.messages['0xa3'].data:
            self.analog_input_1 = int.from_bytes(
                self.bus.messages['0xa3'].data[0:2], byteorder='little', signed=True) / 100
            self.analog_input_2 = int.from_bytes(
                self.bus.messages['0xa3'].data[2:4], byteorder='little', signed=True) / 100
            self.analog_input_3 = int.from_bytes(
                self.bus.messages['0xa3'].data[4:6], byteorder='little', signed=True) / 100
            self.analog_input_4 = int.from_bytes(
                self.bus.messages['0xa3'].data[6:], byteorder='little', signed=True) / 100
        if self.bus.messages['0xa9'].data:
            self.one_five_voltage_ref = int.from_bytes(
                self.bus.messages['0xa9'].data[0:2], byteorder='little', signed=True) / 100
            self.two_five_voltage_ref = int.from_bytes(
                self.bus.messages['0xa9'].data[2:4], byteorder='little', signed=True) / 100
            self.five_voltage_ref = int.from_bytes(
                self.bus.messages['0xa9'].data[4:6], byteorder='little', signed=True) / 100
            self.twelve_system_voltage = int.from_bytes(
                self.bus.messages['0xa9'].data[6:], byteorder='little', signed=True) / 100

    def convert_high_voltages(self) -> None:
        if self.bus.messages['0xa7'].data:
            self.dc_bus_voltage = int.from_bytes(
                self.bus.messages['0xa7'].data[0:2], byteorder='little', signed=True) / 10
            self.output_voltage = int.from_bytes(
                self.bus.messages['0xa7'].data[2:4], byteorder='little', signed=True) / 10
            self.vab_vd_voltage = int.from_bytes(
                self.bus.messages['0xa7'].data[4:6], byteorder='little', signed=True) / 10
            self.vbc_vq_voltage = int.from_bytes(
                self.bus.messages['0xa7'].data[6:], byteorder='little', signed=True) / 10

    def convert_currents(self) -> None:
        if self.bus.messages['0xa6'].data:
            self.phase_a_current = int.from_bytes(
                self.bus.messages['0xa6'].data[0:2], byteorder='little', signed=True) / 10
            self.phase_b_current = int.from_bytes(
                self.bus.messages['0xa6'].data[2:4], byteorder='little', signed=True) / 10
            self.phase_c_current = int.from_bytes(
                self.bus.messages['0xa6'].data[4:6], byteorder='little', signed=True) / 10
            self.dc_bus_current = int.from_bytes(
                self.bus.messages['0xa6'].data[6:], byteorder='little', signed=True) / 10
        if self.bus.messages['0xa8'].data:
            self.id_feedback = int.from_bytes(
                self.bus.messages['0xa8'].data[4:6], byteorder='little', signed=True) / 10
            self.iq_feedback = int.from_bytes(
                self.bus.messages['0xa8'].data[6:], byteorder='little', signed=True) / 10

    def convert_angles(self) -> None:
        if self.bus.messages['0xa5'].data:
            self.motor_angle = int.from_bytes(
                self.bus.messages['0xa5'].data[0:2], byteorder='little', signed=True) / 10
            self.delta_filter_resolved = int.from_bytes(
                self.bus.messages['0xa5'].data[6:], byteorder='little', signed=True) / 10

    def convert_booleans(self) -> None:
        BIT_0 = 1<<0
        BIT_1 = 1<<1
        BIT_2 = 1<<2
        BIT_3 = 1<<3
        BIT_4 = 1<<4
        BIT_5 = 1<<5
        BIT_6 = 1<<6
        BIT_7 = 1<<7
        if self.bus.messages['0xa4']:
            digital_input_status = int.from_bytes(
                self.bus.messages['0xa4'].data[0:], byteorder='little', signed=False)
            self.digital_input_1 = bool(digital_input_status & BIT_0)
            self.digital_input_2 = bool(digital_input_status & BIT_1)
            self.digital_input_3 = bool(digital_input_status & BIT_2)
            self.digital_input_4 = bool(digital_input_status & BIT_3)
            self.digital_input_5 = bool(digital_input_status & BIT_4)
            self.digital_input_6 = bool(digital_input_status & BIT_5)
            self.digital_input_7 = bool(digital_input_status & BIT_6)
            self.digital_input_8 = bool(digital_input_status & BIT_7)

    def convert_torques(self) -> None:
        if self.bus.messages['0xa2'].data:
            self.torque_shudder = int.from_bytes(
                self.bus.messages['0xa2'].data[6:], byteorder='little', signed=True) / 10
        if self.bus.messages['0xac'].data:
            self.commanded_torque = int.from_bytes(
                self.bus.messages['0xac'].data[0:2], byteorder='little', signed=True) / 10
            self.torque_feedback = int.from_bytes(
                self.bus.messages['0xac'].data[2:4], byteorder='little', signed=True) / 10


if __name__ == "__main__":
    import can
    bus = can_manager.CanManager('vcan0')
    control = DTSControl(bus)
    telemetry = DTSTelemetry(bus)
    telemetry.bus.read_message_config('dts', 'message_config.json')

    motorConfiguration = {
        'torque': 2000,
        'speed': 0,
        'direction': 90,
        'inverterEnable': 1,
        'inverterDischarge': 0,
        'speedModeEnable': 0,
        'commandedTorqueLimit': 5000
    }

    control.configure_motor(motorConfiguration)
    while True:
        control.send_motor_command()
        current_message = telemetry.bus.read_bus()
        telemetry.bus.assign_message_data(current_message)
        telemetry.convert_low_voltages()
        print(telemetry.one_five_voltage_ref)
        print(telemetry.two_five_voltage_ref)
        print(telemetry.five_voltage_ref)
        print(telemetry.twelve_system_voltage)
