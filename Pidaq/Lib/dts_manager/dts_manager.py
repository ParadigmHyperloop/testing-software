from enum import Enum

from can_manager import can_manager


class InverterMode(Enum):
    ''' Used to indicate the desired inverter mode'''
    Torque = 0
    Speed = 1


class InverterDirection(Enum):
    ''' Used to indicate the desired inverter direction'''
    Reverse = 0
    Forward = 1


class InverterEnable(Enum):
    ''' Used to indicate whether or not the inverter is to be enabled'''
    Inverter_Off = 0
    Inverter_On = 1


class InverterDischarge(Enum):
    ''' Used to indicate whether or not the inverter is discharging'''
    Disable = 0
    Enable = 1


class MotorConfig():
    ''' Structure to hold motor configuration info to be sent in config message

    Fields:
        torque_command (float): The desired motor torque
        speed_command (float): The desired motor speed
        direction (InverterDirection)
        inverter_enable (InverterEnable)
        inverter_discharge (InverterDischarge)
        mode (InverterMode): The desired inverter mode, whichever mode is not selected, the
                             respective command will be set to 0
        commanded_torque_limit (float): torque that the motor will not exceed,
                                        defaults to 0, which will read default
                                        torque limit from EEPROM
    '''

    def __init__(self, command=0.0, direction=InverterDirection.Forward, enable=InverterEnable.Inverter_Off,
                 discharge=InverterDischarge.Disable, mode=InverterMode.Torque, commanded_torque_limit=0.0):
        self.torque_command = command if mode == InverterMode.Torque else 0.0
        self.speed_command = command if mode == InverterMode.Speed else 0.0
        self.direction = direction.value
        self.inverter_enable = enable.value
        self.inverter_discharge = discharge.value
        self.mode = mode.value
        self.commanded_torque_limit = commanded_torque_limit

class DTS():
    def __init__(self, bus: can_manager.CanManager):
        self.control = DTS.DTSControl(bus)
        self.telemetry = DTS.DTSTelemetry(bus)
        # Add state here if necessary in future

    class DTSControl():
        ''' Handles control aspects of DTS motor/inverter

        Fields:
            bus (can_manager.CanManager): instance of CanManager to communicate with Can bus
            torque_command (int)
            speed_command (int)
            direction_command (int)
            inverter_enable (int)
            inverter_discharge (int)
            speed_mode_enable (int)
            mode (int)
            commanded_torque_limit (int)

        Methods:
            configure_motor(self, configuration=MotorConfig()) -> None:
                When given a MotorConfig object, this method reads all the properties,
                converts them to bytes which can then be sent in the command message

            send_motor_command(self):
                Sends motor command over the can bus with the correct message ID to be interpreted
                by the DTS inverter
        '''

        def __init__(self, bus: can_manager.CanManager):
            self.bus = bus

            # Default can offset is 160, can be changed in EEPROM
            self.message_offset = 160
            self.command_id = self.message_offset + 32

        def configure_motor(self, configuration=MotorConfig()) -> None:
            ''' Configures the motor configuration message'''
            self.torque_command = int(
                configuration.torque_command * 10).to_bytes(2, 'little')
            # Extract commands from dict
            self.speed_command = int(
                configuration.speed_command * 10).to_bytes(2, 'little')
            self.direction_command = int(
                configuration.direction).to_bytes(1, 'little')
            self.inverter_enable = int(configuration.inverter_enable)
            self.inverter_discharge = int(configuration.inverter_discharge)
            self.speed_mode_enable = int(configuration.mode)
            self.mode = ((int(self.speed_mode_enable) << 2) +
                        (int(self.inverter_discharge) << 1) + (int(self.inverter_enable) << 0)).to_bytes(1, 'little')
            self.commanded_torque_limit = int(
                configuration.commanded_torque_limit * 10).to_bytes(2, 'little')

        def send_motor_command_config(self) -> None:
            ''' Send motor command over the can bus

            Note: This method should not be called until after the configure_motor method has been called
                at least once to configure a command message.
            '''
            command_list = self.torque_command + self.speed_command + \
                self.direction_command + self.mode + self.commanded_torque_limit
            self.bus.send_message(self.command_id, command_list)

        def send_motor_command(self, command, mode=InverterMode.Torque):
            speed_command = int(command if mode == InverterMode.Speed else 0).to_bytes(2, 'little')
            torque_commmand = (command if mode == InverterMode.Torque else 0).to_bytes(2, 'little')
            mode = ((int(self.mode.value) << 2) +
                   (int(self.inverter_discharge) << 1) + (int(self.inverter_enable) << 0)).to_bytes(1, 'little')
            command_list = torque_commmand + speed_command + \
                self.direction_command + mode + self.commanded_torque_limit
            self.bus.send_message(self.command_id, command_list)

    class DTSTelemetry():
        ''' Handles the telemetry and data acquisition from the DTS motor/inverter

        Fields:
            See __init__ for fields, all possible data fields are stored within the class

        Methods:
        Note: each method converts a different set of data, depending on the conversion factor
            defined in the CAN message format manual for the inverter

            convert_angles(self)
            convert_booleans(self)
            convert_currents(self)
            convert_high_voltages(self)
            convert_low_voltages(self)
            convert_torques(self)
            convert_temperatures(self)
        '''

        def __init__(self, bus: can_manager.CanManager):
            ''' Takes reference to a CanManager instance to be used for receiving can messages'''
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
            
            # Default can offset is 160, can be changed in EEPROM
            self.default_can_offset = 160
            self.temp1_id = self.default_can_offset
            self.temp2_id = self.default_can_offset + 1
            self.temp3_id = self.default_can_offset + 2
            self.analog_inputs_id = self.default_can_offset + 3
            self.digital_input_status_id = self.default_can_offset + 4
            self.motor_position_id = self.default_can_offset + 5
            self.current_info_id = self.default_can_offset + 6
            self.voltage_info_id = self.default_can_offset + 7
            self.flux_info_id = self.default_can_offset + 8
            self.internal_voltages_id = self.default_can_offset + 9
            self.internal_states_id = self.default_can_offset + 10
            self.fault_codes_id = self.default_can_offset + 11
            self.torque_timer_id = self.default_can_offset + 12
            self.modulation_index_id = self.default_can_offset + 13
        
        def get_temp1_data(self):
            return self.bus.messages[self.temp1_id].data
        
        def get_temp2_data(self):
            return self.bus.messages[self.temp2_id].data
        
        def get_temp3_data(self):
            return self.bus.messages[self.temp3_id].data

        def get_analog_input_voltages_data(self):
            return self.bus.messages[self.analog_inputs_id].data
        
        def get_digital_input_status_data(self):
            return self.bus.messages[self.digital_input_status_id].data
        
        def get_motor_position_data(self):
            return self.bus.messages[self.motor_position_id].data

        def get_current_data(self):
            return self.bus.messages[self.current_info_id].data

        def get_voltage_data(self):
            return self.bus.messages[self.voltage_info_id].data

        def get_flux_data(self):
            return self.bus.messages[self.flux_info_id].data

        def get_internal_voltages_data(self):
            return self.bus.messages[self.internal_voltages_id].data
        
        def get_internal_states_data(self):
            return self.bus.messages[self.internal_states_id].data

        def get_faults_data(self):
            return self.bus.messages[self.fault_codes_id].data

        def get_torque_timer_data(self):
            return self.bus.messages[self.torque_timer_id].data
        
        def get_modulation_index_data(self):
            return self.bus.messages[self.modulation_index_id].data

        def convert_temperatures(self) -> None:
            if self.get_temp1_data():
                self.module_a_temperature = int.from_bytes(
                    self.get_temp1_data()[0:2], byteorder='little', signed=True) / 10
                self.module_b_temperature = int.from_bytes(
                    self.get_temp1_data()[2:4], byteorder='little', signed=True) / 10
                self.module_c_temperature = int.from_bytes(
                    self.get_temp1_data()[4:6], byteorder='little', signed=True) / 10
                self.gate_driver_board_temperature = int.from_bytes(
                    self.get_temp1_data()[6:], byteorder='little', signed=True) / 10
            if self.get_temp2_data():
                self.control_board_temperature = int.from_bytes(
                    self.get_temp2_data()[0:2], byteorder='little', signed=True) / 10
                self.rtd_1_temperature = int.from_bytes(
                    self.get_temp2_data()[2:4], byteorder='little', signed=True) / 10
                self.rtd_2_temperature = int.from_bytes(
                    self.get_temp2_data()[4:6], byteorder='little', signed=True) / 10
                self.rtd_3_temperature = int.from_bytes(
                    self.get_temp2_data()[6:], byteorder='little', signed=True) / 10
            if self.get_temp3_data():
                self.rtd_4_temperature = int.from_bytes(
                    self.get_temp3_data()[0:2], byteorder='little', signed=True) / 10
                self.rtd_5_temperature = int.from_bytes(
                    self.get_temp3_data()[2:4], byteorder='little', signed=True) / 10
                self.motor_temperature = int.from_bytes(
                    self.get_temp3_data()[4:6], byteorder='little', signed=True) / 10

        def convert_low_voltages(self) -> None:
            if self.get_analog_input_voltages_data():
                self.analog_input_1 = int.from_bytes(
                    self.get_analog_input_voltages_data()[0:2], byteorder='little', signed=True) / 100
                self.analog_input_2 = int.from_bytes(
                    self.get_analog_input_voltages_data()[2:4], byteorder='little', signed=True) / 100
                self.analog_input_3 = int.from_bytes(
                    self.get_analog_input_voltages_data()[4:6], byteorder='little', signed=True) / 100
                self.analog_input_4 = int.from_bytes(
                    self.get_analog_input_voltages_data()[6:], byteorder='little', signed=True) / 100
            if self.get_internal_voltages_data():
                self.one_five_voltage_ref = int.from_bytes(
                    self.get_internal_voltages_data()[0:2], byteorder='little', signed=True) / 100
                self.two_five_voltage_ref = int.from_bytes(
                    self.get_internal_voltages_data()[2:4], byteorder='little', signed=True) / 100
                self.five_voltage_ref = int.from_bytes(
                    self.get_internal_voltages_data()[4:6], byteorder='little', signed=True) / 100
                self.twelve_system_voltage = int.from_bytes(
                    self.get_internal_voltages_data()[6:], byteorder='little', signed=True) / 100

        def convert_high_voltages(self) -> None:
            if self.get_voltage_data():
                self.dc_bus_voltage = int.from_bytes(
                    self.get_voltage_data()[0:2], byteorder='little', signed=True) / 10
                self.output_voltage = int.from_bytes(
                    self.get_voltage_data()[2:4], byteorder='little', signed=True) / 10
                self.vab_vd_voltage = int.from_bytes(
                    self.get_voltage_data()[4:6], byteorder='little', signed=True) / 10
                self.vbc_vq_voltage = int.from_bytes(
                    self.get_voltage_data()[6:], byteorder='little', signed=True) / 10

        def convert_currents(self) -> None:
            if self.get_current_data():
                self.phase_a_current = int.from_bytes(
                    self.get_current_data()[0:2], byteorder='little', signed=True) / 10
                self.phase_b_current = int.from_bytes(
                    self.get_current_data()[2:4], byteorder='little', signed=True) / 10
                self.phase_c_current = int.from_bytes(
                    self.get_current_data()[4:6], byteorder='little', signed=True) / 10
                self.dc_bus_current = int.from_bytes(
                    self.get_current_data()[6:], byteorder='little', signed=True) / 10
            if self.get_flux_data():
                self.id_feedback = int.from_bytes(
                    self.get_flux_data()[4:6], byteorder='little', signed=True) / 10
                self.iq_feedback = int.from_bytes(
                    self.get_flux_data()[6:], byteorder='little', signed=True) / 10

        def convert_angles(self) -> None:
            if self.get_motor_position_data():
                self.motor_angle = int.from_bytes(
                    self.get_motor_position_data(), byteorder='little', signed=True) / 10
                self.delta_filter_resolved = int.from_bytes(
                    self.get_motor_position_data(), byteorder='little', signed=True) / 10

        def convert_booleans(self) -> None:
            BIT_0 = 1 << 0
            BIT_1 = 1 << 1
            BIT_2 = 1 << 2
            BIT_3 = 1 << 3
            BIT_4 = 1 << 4
            BIT_5 = 1 << 5
            BIT_6 = 1 << 6
            BIT_7 = 1 << 7
            if self.get_digital_input_status_data():
                digital_input_status = int.from_bytes(
                    self.get_digital_input_status_data()[0:], byteorder='little', signed=False)
                self.digital_input_1 = bool(digital_input_status & BIT_0)
                self.digital_input_2 = bool(digital_input_status & BIT_1)
                self.digital_input_3 = bool(digital_input_status & BIT_2)
                self.digital_input_4 = bool(digital_input_status & BIT_3)
                self.digital_input_5 = bool(digital_input_status & BIT_4)
                self.digital_input_6 = bool(digital_input_status & BIT_5)
                self.digital_input_7 = bool(digital_input_status & BIT_6)
                self.digital_input_8 = bool(digital_input_status & BIT_7)

        def convert_torques(self) -> None:
            if self.get_temp3_data():
                self.torque_shudder = int.from_bytes(
                    self.get_temp3_data()[6:], byteorder='little', signed=True) / 10
            if self.get_torque_timer_data():
                self.commanded_torque = int.from_bytes(
                    self.get_torque_timer_data()[0:2], byteorder='little', signed=True) / 10
                self.torque_feedback = int.from_bytes(
                    self.get_torque_timer_data()[2:4], byteorder='little', signed=True) / 10


if __name__ == "__main__":
    import random
    bus = can_manager.CanManager('vcan0')
    dts = DTS(bus)
    bus.read_message_config('dts', 'message_config.json')

    motorConfiguration = MotorConfig(200, InverterDirection.Forward, InverterEnable.Inverter_On,
                                     InverterDischarge.Enable, InverterMode.Torque, 400)

    dts.control.configure_motor(motorConfiguration)
    dts.control.send_motor_command_config()
    while True:
        current_message = dts.telemetry.bus.read_bus()
        dts.telemetry.bus.assign_message_data(current_message)
        dts.telemetry.convert_low_voltages()
        print(dts.telemetry.one_five_voltage_ref)
        print(dts.telemetry.two_five_voltage_ref)
        print(dts.telemetry.five_voltage_ref)
        print(dts.telemetry.twelve_system_voltage)
        dts.control.send_motor_command(random.randrange(190, 220), InverterMode.Torque)
