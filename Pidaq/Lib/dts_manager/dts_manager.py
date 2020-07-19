import time
from collections import deque
from enum import Enum

import can

from can_manager import can_manager


class InverterMode(Enum):
    """ Used to indicate the desired inverter mode"""
    Torque = 0
    Speed = 1


class InverterDirection(Enum):
    """ Used to indicate the desired inverter direction"""
    Reverse = 0
    Forward = 1


class InverterEnable(Enum):
    """ Used to indicate whether or not the inverter is to be enabled"""
    Inverter_Off = 0
    Inverter_On = 1


class InverterDischarge(Enum):
    """ Used to indicate whether or not the inverter is discharging"""
    Disable = 0
    Enable = 1


class MotorConfig():
    """ Structure to hold motor configuration info to be sent in config message

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
        duration (float): Time duration that the message will be sent on the bus for
    """

    def __init__(self, command=0.0, direction=InverterDirection.Forward, enable=InverterEnable.Inverter_Off,
                 discharge=InverterDischarge.Disable, mode=InverterMode.Torque, commanded_torque_limit=0.0, duration=None):
        self.torque_command = command if mode == InverterMode.Torque else 0.0
        self.speed_command = command if mode == InverterMode.Speed else 0.0
        self.direction = direction.value
        self.inverter_enable = enable.value
        self.inverter_discharge = discharge.value
        self.mode = mode.value
        self.commanded_torque_limit = commanded_torque_limit
        self.duration = duration


class MotorCommand():
    """ Structure to hold command info to be sent after initial configuration"""

    def __init__(self, command=0.0, duration=None):
        self.command = command
        self.duration = duration


class DTS():
    def __init__(self, bus: can_manager.CanManager):
        self.control = DTS.DTSControl(bus)
        self.telemetry = DTS.DTSTelemetry(bus)
        # Add state here if necessary in future

    class DTSControl():
        """ Handles control aspects of DTS motor/inverter

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
            message_offset (int)
            command_id (int)

        Methods:
            configure_motor(self, configuration=MotorConfig()) -> None:
                When given a MotorConfig object, this method reads all the properties,
                converts them to bytes which can then be sent in the command message

            send_motor_command(self):
                Sends motor command over the can bus with the correct message ID to be interpreted
                by the DTS inverter
        """

        def __init__(self, bus: can_manager.CanManager):
            self.bus = bus

            # Default can offset is 160, can be changed in EEPROM
            self.message_offset = 160
            self.command_id = self.message_offset + 32

            self.current_command_message = None
            self.start_time = None
            self.commands_finished = False

        def configure_motor(self, configuration=MotorConfig()) -> None:
            """ Configures the motor configuration message"""
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
            """ Send motor command over the can bus

            Note: This method should not be called until after the configure_motor method has been called
                at least once to configure a command message.
            """
            command_list = self.torque_command + self.speed_command + \
                self.direction_command + self.mode + self.commanded_torque_limit
            self.bus.send_message(self.command_id, command_list)

        def send_motor_command(self, command: float, mode=InverterMode.Torque, duration=None):
            """ Sends a motor command using existing info plus new speed/torque command and mode

            Uses all existing message configuration except for speed/torque command, and mode.
            Can be used to issue subsequent commands after the motor has been configured intially

            Args:
                command (float): New speed/torque command, depending on the mode
                mode (InverterMode)
                duration (float): duration for which the message should be sent
            """
            speed_command = int(
                command * 10 if mode == InverterMode.Speed else 0).to_bytes(2, 'little')
            torque_commmand = (
                command * 10 if mode == InverterMode.Torque else 0).to_bytes(2, 'little')
            mode = ((int(mode.value) << 2) +
                    (int(self.inverter_discharge) << 1) + (int(self.inverter_enable) << 0)).to_bytes(1, 'little')
            command_list = torque_commmand + speed_command + \
                self.direction_command + mode + self.commanded_torque_limit
            message = can.Message(arbitration_id=192, data=command_list)
            if self.current_command_message is not None:
                self.current_command_message.stop()
            self.current_command_message = self.bus.send_message_periodic(message, duration)

        def send_test_commands(self, initial_config: MotorConfig=MotorConfig(), commands=None):
            """ Sends all the commands for the test, for the specified durations

            Args:
                initial_config (MotorConfig): MotorConfig object with initial motor configuration
                commands (List[MotorCommand]): List of motor command objects, which will be executed in order
                                               for the specified duration
            """
            # Initial setup branch, only executes the first time the method is ran
            if self.start_time is None:
                self.configure_motor(initial_config)
                self.send_motor_command_config()
                self.messages = deque()
                for command in commands:
                    self.messages.append(command)
                self.current_command = self.messages.popleft()
                self.start_time = time.time()
                self.send_motor_command(self.current_command.command)

            # Compares the command duration to the time that has elapsed since the command started
            elif self.current_command.duration < time.time() - self.start_time:

                # No messages left to send
                if len(self.messages) == 0:
                    self.commands_finished = True
                    try:
                        self.current_command_message.stop()
                    finally:
                        return self.commands_finished

                # Get next message, reset start_time, and send message
                self.current_command = self.messages.popleft()
                self.start_time = time.time()
                self.send_motor_command(self.current_command.command)
            else:
                return self.commands_finished

    class DTSTelemetry():
        """ Handles the telemetry and data acquisition from the DTS motor/inverter

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
            Data Getters:
                get_analog_input_voltages_data(self)
                get_current_data(self)
                get_digital_input_status_data(self)
                get_faults_data(self)
                get_flux_data(self)
                get_internal_states_data(self)
                get_internal_voltages_data(self)
                get_modulation_index_data(self)
                get_motor_position_data(self)
                get_temp1_data(self)
                get_temp2_data(self)
                get_temp3_data(self)
                get_torque_timer_data(self)
                get_voltage_data(self)
        """

        def __init__(self, bus: can_manager.CanManager):
            """ Takes reference to a CanManager instance to be used for receiving can messages"""
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

            # Sets of related ids for quick lookups
            self.temp_ids = set([self.temp1_id, self.temp2_id, self.temp3_id])
            self.low_voltage_ids = set([self.analog_inputs_id, self.internal_voltages_id])
            self.current_ids = set([self.current_info_id, self.flux_info_id, self.modulation_index_id])
            self.torque_ids = set([self.motor_position_id, self.torque_timer_id])

        def get_conversion_factor(self, message_id: int):
            return self.bus.messages[message_id].conversion_factor

        def get_temp1_data(self, start=0, stop=8):
            if self.bus.messages[self.temp1_id].data:
                return self.bus.messages[self.temp1_id].data[start:stop]
            else:
                return None

        def get_temp2_data(self, start=0, stop=8):
            if self.bus.messages[self.temp2_id].data:
                return self.bus.messages[self.temp2_id].data[start:stop]
            else:
                return None

        def get_temp3_data(self, start=0, stop=8):
            if self.bus.messages[self.temp3_id].data:
                return self.bus.messages[self.temp3_id].data[start:stop]
            else:
                return None

        def get_analog_input_voltages_data(self, start=0, stop=8):
            if self.bus.messages[self.analog_inputs_id].data:
                return self.bus.messages[self.analog_inputs_id].data[start:stop]
            else:
                return None

        def get_digital_input_status_data(self, start=0, stop=8):
            if self.bus.messages[self.digital_input_status_id].data:
                return self.bus.messages[self.digital_input_status_id].data[start:stop]
            else:
                return None

        def get_motor_position_data(self, start=0, stop=8):
            if self.bus.messages[self.motor_position_id].data:
                return self.bus.messages[self.motor_position_id].data[start:stop]
            else:
                return None

        def get_current_data(self, start=0, stop=8):
            if self.bus.messages[self.current_info_id].data:
                return self.bus.messages[self.current_info_id].data[start:stop]
            else:
                return None

        def get_voltage_data(self, start=0, stop=8):
            if self.bus.messages[self.voltage_info_id].data:
                return self.bus.messages[self.voltage_info_id].data[start:stop]
            else:
                return None

        def get_flux_data(self, start=0, stop=8):
            if self.bus.messages[self.flux_info_id].data:
                return self.bus.messages[self.flux_info_id].data[start:stop]
            else:
                return None

        def get_internal_voltages_data(self, start=0, stop=8):
            if self.bus.messages[self.internal_voltages_id].data:
                return self.bus.messages[self.internal_voltages_id].data[start:stop]
            else:
                return None

        def get_internal_states_data(self, start=0, stop=8):
            if self.bus.messages[self.internal_states_id].data:
                return self.bus.messages[self.internal_states_id].data[start:stop]
            else:
                return None

        def get_faults_data(self, start=0, stop=8):
            if self.bus.messages[self.fault_codes_id].data:
                return self.bus.messages[self.fault_codes_id].data[start:stop]
            else:
                return None

        def get_torque_timer_data(self, start=0, stop=8):
            if self.bus.messages[self.torque_timer_id].data:
                return self.bus.messages[self.torque_timer_id].data[start:stop]
            else:
                return None

        def get_modulation_index_data(self, start=0, stop=8):
            if self.bus.messages[self.modulation_index_id].data:
                return self.bus.messages[self.modulation_index_id].data[start:stop]
            else:
                return None

        def update_temperatures(self) -> None:
            if self.get_temp1_data():
                self.module_a_temperature = int.from_bytes(
                    self.get_temp1_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.temp1_id)
                self.module_b_temperature = int.from_bytes(
                    self.get_temp1_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.temp1_id)
                self.module_c_temperature = int.from_bytes(
                    self.get_temp1_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.temp1_id)
                self.gate_driver_board_temperature = int.from_bytes(
                    self.get_temp1_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.temp1_id)
            if self.get_temp2_data():
                self.control_board_temperature = int.from_bytes(
                    self.get_temp2_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.temp2_id)
                self.rtd_1_temperature = int.from_bytes(
                    self.get_temp2_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.temp2_id)
                self.rtd_2_temperature = int.from_bytes(
                    self.get_temp2_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.temp2_id)
                self.rtd_3_temperature = int.from_bytes(
                    self.get_temp2_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.temp2_id)
            if self.get_temp3_data():
                self.rtd_4_temperature = int.from_bytes(
                    self.get_temp3_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.temp3_id)['temp']
                self.rtd_5_temperature = int.from_bytes(
                    self.get_temp3_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.temp3_id)['temp']
                self.motor_temperature = int.from_bytes(
                    self.get_temp3_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.temp3_id)['temp']

        def update_low_voltages(self) -> None:
            if self.get_analog_input_voltages_data():
                self.analog_input_1 = int.from_bytes(
                    self.get_analog_input_voltages_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.analog_inputs_id)
                self.analog_input_2 = int.from_bytes(
                    self.get_analog_input_voltages_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.analog_inputs_id)
                self.analog_input_3 = int.from_bytes(
                    self.get_analog_input_voltages_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.analog_inputs_id)
                self.analog_input_4 = int.from_bytes(
                    self.get_analog_input_voltages_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.analog_inputs_id)
            if self.get_internal_voltages_data():
                self.one_five_voltage_ref = int.from_bytes(
                    self.get_internal_voltages_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.internal_voltages_id)
                self.two_five_voltage_ref = int.from_bytes(
                    self.get_internal_voltages_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.internal_voltages_id)
                self.five_voltage_ref = int.from_bytes(
                    self.get_internal_voltages_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.internal_voltages_id)
                self.twelve_system_voltage = int.from_bytes(
                    self.get_internal_voltages_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.internal_voltages_id)

        def update_high_voltages(self) -> None:
            if self.get_voltage_data():
                self.dc_bus_voltage = int.from_bytes(
                    self.get_voltage_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.voltage_info_id)
                self.output_voltage = int.from_bytes(
                    self.get_voltage_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.voltage_info_id)
                self.vab_vd_voltage = int.from_bytes(
                    self.get_voltage_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.voltage_info_id)
                self.vbc_vq_voltage = int.from_bytes(
                    self.get_voltage_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.voltage_info_id)

        def update_currents(self) -> None:
            if self.get_current_data():
                self.phase_a_current = int.from_bytes(
                    self.get_current_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.current_info_id)
                self.phase_b_current = int.from_bytes(
                    self.get_current_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.current_info_id)
                self.phase_c_current = int.from_bytes(
                    self.get_current_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.current_info_id)
                self.dc_bus_current = int.from_bytes(
                    self.get_current_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.current_info_id)
            if self.get_flux_data():
                self.id_feedback = int.from_bytes(
                    self.get_flux_data(4, 6), byteorder='little', signed=True) / self.get_conversion_factor(self.flux_info_id)['current']
                self.iq_feedback = int.from_bytes(
                    self.get_flux_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.flux_info_id)['current']

        def update_angles(self) -> None:
            if self.get_motor_position_data():
                self.motor_angle = int.from_bytes(
                    self.get_motor_position_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.motor_position_id)['angle']
                self.delta_filter_resolved = int.from_bytes(
                    self.get_motor_position_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.motor_position_id)['angle']

        def update_booleans(self) -> None:
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
                    self.get_digital_input_status_data(), byteorder='little', signed=False)
                self.digital_input_1 = bool(digital_input_status & BIT_0)
                self.digital_input_2 = bool(digital_input_status & BIT_1)
                self.digital_input_3 = bool(digital_input_status & BIT_2)
                self.digital_input_4 = bool(digital_input_status & BIT_3)
                self.digital_input_5 = bool(digital_input_status & BIT_4)
                self.digital_input_6 = bool(digital_input_status & BIT_5)
                self.digital_input_7 = bool(digital_input_status & BIT_6)
                self.digital_input_8 = bool(digital_input_status & BIT_7)

        def update_torques(self) -> None:
            if self.get_temp3_data():
                self.torque_shudder = int.from_bytes(
                    self.get_temp3_data(6, 8), byteorder='little', signed=True) / self.get_conversion_factor(self.temp3_id)['torque']
            if self.get_torque_timer_data():
                self.commanded_torque = int.from_bytes(
                    self.get_torque_timer_data(0, 2), byteorder='little', signed=True) / self.get_conversion_factor(self.torque_timer_id)
                self.torque_feedback = int.from_bytes(
                    self.get_torque_timer_data(2, 4), byteorder='little', signed=True) / self.get_conversion_factor(self.torque_timer_id)

        def update_data(self):
            """ Calls the update methods as necessary
 
            Reads the can bus for the current message, assigns the message to the correct
            sensor reading object, and calls the respective update methods to update data
            fields based on the data type stored in the message
            """
            current_message = self.bus.read_bus()
            self.bus.assign_message_data(current_message)
            message_id = current_message.arbitration_id
            if message_id in self.temp_ids:
                self.update_temperatures()
                self.update_torques()
            elif message_id in self.low_voltage_ids:
                self.update_low_voltages()
            elif message_id == self.digital_input_status_id:
                self.update_booleans()
            elif message_id in self.current_ids:
                self.update_currents()
            elif message_id == self.voltage_info_id:
                self.update_high_voltages()
            elif message_id in self.current_ids:
                self.update_torques()
                self.update_angles()


if __name__ == "__main__":
    import random
    bus = can_manager.CanManager('vcan0')
    dts = DTS(bus)
    bus.read_message_config('dts', 'message_config.json')

    motorConfiguration = MotorConfig(200, InverterDirection.Forward, InverterEnable.Inverter_On,
                                     InverterDischarge.Enable, InverterMode.Torque, 400)

    motorCommands = [MotorCommand(300, 5), MotorCommand(400, 5), MotorCommand(500, 5), MotorCommand(400, 5), MotorCommand(100, 5)]

    while True:
        dts.control.send_test_commands(motorConfiguration, motorCommands)
        dts.telemetry.update_data()
        print('Analog Input 1: {}'.format(dts.telemetry.analog_input_1))
        print('Analog Input 2: {}'.format(dts.telemetry.analog_input_2))
        print('Analog Input 3: {}'.format(dts.telemetry.analog_input_3))
        print('Analog Input 4: {}'.format(dts.telemetry.analog_input_4))
        print('Commanded Torque: {}'.format(dts.telemetry.commanded_torque))
        print('Control Board Temperature: {}'.format(dts.telemetry.control_board_temperature))
        print('DC Bus Voltage: {}'.format(dts.telemetry.dc_bus_voltage))
        print('Delta Filter Resolved: {}'.format(dts.telemetry.delta_filter_resolved))
        print('Gate Driver Board Temp: {}'.format(dts.telemetry.gate_driver_board_temperature))
        print('Id Feedback: {}'.format(dts.telemetry.id_feedback))
        print('Iq Feedback: {}'.format(dts.telemetry.iq_feedback))
        print('Module A Temperature: {}'.format(dts.telemetry.module_a_temperature))
        print('Module B Temperature: {}'.format(dts.telemetry.module_b_temperature))
        print('Module C Temperature: {}'.format(dts.telemetry.module_c_temperature))
        print('Motor Angle: {}'.format(dts.telemetry.motor_angle))
        print('1.5V Ref Voltage: {}'.format(dts.telemetry.one_five_voltage_ref))
        print('Output Voltage: {}'.format(dts.telemetry.output_voltage))
        print('RTD 1 Temp: {}'.format(dts.telemetry.rtd_1_temperature))
        print('RTD 2 Temp: {}'.format(dts.telemetry.rtd_2_temperature))
        print('RTD 3 Temp: {}'.format(dts.telemetry.rtd_3_temperature))
        print('RTD 4 Temp: {}'.format(dts.telemetry.rtd_4_temperature))
        print('RTD 5 Temp: {}'.format(dts.telemetry.rtd_5_temperature))
        print('Torque Shudder: {}'.format(dts.telemetry.torque_shudder))
        print('12V System Voltage: {}'.format(dts.telemetry.twelve_system_voltage))
        print('2.5V Ref Voltage: {}'.format(dts.telemetry.two_five_voltage_ref))
        print('Vab Vd Voltage: {}'.format(dts.telemetry.vab_vd_voltage))
        print('Vbc Vq Voltage: {}\n'.format(dts.telemetry.vbc_vq_voltage))
