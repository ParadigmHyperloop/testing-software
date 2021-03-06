import sys
import time
from enum import Enum
from random import random

import can

from can_manager import can_manager


class DTSSimulator:
    """ Class for simulating the behaviour of the DTS motor/inverter

    The majority of the data sent over the can bus contains spoofed data, however
    the simulator is able to correctly interpret command messages, and send back the correct
    data based on the command message received.

    Fields:
        See methods, too many to list here, but all are data that the real inverter
        sends through CAN messages

    Methods:
        check_can_timeout(self, message)
        display_currents(self)
        display_motor_info(self)
        display_temps(self)
        display_voltages(self)
        read_configuration_message(self)
        send_information_messages_10Hz(self)
        send_information_messages_100Hz(self)
        update_analog_input_voltages(self)
        update_current_information(self)
        update_digital_input_status(self) - To be defined
        update_fault_codes(self) - To be defined
        update_flux_information(self)
        update_internal_states(self) - To be defined
        update_internal_voltages(self)
        update_modulation_index(self) - To be defined
        update_motor_position_information(self)
        update_temperature1(self)
        update_temperature2(self)
        update_temperature3(self)
        update_torque_timer_information(self)
        update_voltage_information(self)
    """

    def __init__(self, bus_name: str):
        # Configure bus
        self.can_bus = can_manager.CanManager(bus_name)

        # Configure messages
        self.temperature1 = can.Message(arbitration_id=160, dlc=8)
        self.temperature2 = can.Message(arbitration_id=161, dlc=8)
        self.temperature3 = can.Message(arbitration_id=162, dlc=8)
        self.analog_input_voltages = can.Message(arbitration_id=163, dlc=8)
        self.digital_input_status = can.Message(arbitration_id=164, dlc=8)
        self.motor_position_information = can.Message(
            arbitration_id=165,
            dlc=8
        )
        self.current_information = can.Message(arbitration_id=166, dlc=8)
        self.voltage_information = can.Message(arbitration_id=167, dlc=8)
        self.flux_information = can.Message(arbitration_id=168, dlc=8)
        self.internal_voltages = can.Message(arbitration_id=169, dlc=8)
        self.internal_states = can.Message(arbitration_id=170, dlc=8)
        self.fault_codes = can.Message(arbitration_id=171, dlc=8)
        self.torque_timer_info = can.Message(arbitration_id=172, dlc=8)
        self.modulation_index_flux_weakening = can.Message(
            arbitration_id=173,
            dlc=8
        )
        self.firmware_information = can.Message(arbitration_id=174, dlc=8)
        self.last_received_command_message = 0

    def __str__(self):
        return f'''
        Current DTS Sim State:
        {self.display_temps()} 

        {self.display_voltages()}

        {self.display_currents()}

        {self.display_motor_info()}
        '''

    def display_temps(self):
        return '''
        Current Temperature Status:
        Module A Temperature: {:.2f}
        Module B Temperature: {:.2f}
        Module C Temperature: {:.2f}
        Gate Driver Board Temperature: {:.2f}
        Control Board Temperature: {:.2f}
        RTD 1 Temperature: {:.2f}
        RTD 2 Temperature: {:.2f}
        RTD 3 Temperature: {:.2f}
        RTD 4 Temperature: {:.2f}
        RTD 5 Temperature: {:.2f}
        Motor Temperature: {:.2f}
        '''.format(self.module_a_temp / 10,
                   self.module_b_temp / 10,
                   self.module_c_temp / 10,
                   self.gate_driver_board_temp / 10,
                   self.control_board_temp / 10,
                   self.rtd_1_temp / 10,
                   self.rtd_2_temp / 10,
                   self.rtd_4_temp / 10,
                   self.rtd_4_temp / 10,
                   self.rtd_5_temp / 10,
                   self.motor_temp / 10)

    def display_voltages(self):
        return '''
        Current Voltage Status:
        Analog Input 1 Voltage: {:.2f}V
        Analog Input 2 Voltage: {:.2f}V
        Analog Input 3 Voltage: {:.2f}V
        Analog Input 4 Voltage: {:.2f}V
        1.5V Reference Voltage: {:.2f}V
        2.5V Reference Voltage: {:.2f}V
        5.0V Reference Voltage: {:.2f}V
        12V System Voltage: {:.2f}V
        DC Bus Voltage: {:.2f}V
        Output Voltage: {:.2f}V
        VAB_Vd Voltage: {:.2f}V
        VBC_Vq Voltage: {:.2f}V
        '''.format(self.analog_input_1 / 100,
                   self.analog_input_2 / 100,
                   self.analog_input_3 / 100,
                   self.analog_input_4 / 100,
                   self.one_five_voltage_ref / 100,
                   self.two_five_voltage_ref / 100,
                   self.five_voltage_ref / 100,
                   self.twelve_system_voltage / 100,
                   self.dc_bus_voltage / 10,
                   self.output_voltage / 10,
                   self.vab_vd_voltage / 10,
                   self.vbc_vq_voltage / 10)

    def display_currents(self):
        return '''
        Current Status:
        Phase A Current: {:.2f}A
        Phase B Current: {:.2f}A
        Phase C Current: {:.2f}A
        DC Bus Current: {:.2f}A
        Id Feedback Current: {:.2f}A
        Iq Feedback Current: {:.2f}A
        '''.format(self.phase_a_current / 10,
                   self.phase_b_current / 10,
                   self.phase_c_current / 10,
                   self.dc_bus_current / 10,
                   self.id_feedback / 10,
                   self.iq_feedback / 10)

    def display_motor_info(self):
        return '''
        Motor Position Information:
        Motor Angle: {:.2f}Degrees
        Motor Speed: {:.2f}RPM
        Electrical Output Frequency: {:.2f}Hz
        Delta Filter Resolved: {:.2f}Degrees
        Commanded Torque: {:.2f} Nm
        '''.format(self.motor_angle / 10,
                   self.motor_speed,
                   self.electrical_output_frequency / 10,
                   self.delta_filter_resolved / 10,
                   self.torque_command)

    def check_can_timeout(self, message: can.Message):
        if self.last_received_command_message == 0:
            self.last_received_command_message = time.time()
        if message is not None and message.arbitration_id == 192:
            self.last_received_command_message = time.time()
        if time.time() - self.last_received_command_message > .5:
            sys.exit()

    def update_temperature1(self):
        self.module_a_temp = 200 + random() * 5.0
        self.module_b_temp = 210 + random() * 4.5
        self.module_c_temp = 205 + random() * 3.7
        self.gate_driver_board_temp = 190 + random() * 6.2
        module_a_temp_bytes = int(self.module_a_temp).to_bytes(2, 'little')
        module_b_temp_bytes = int(self.module_b_temp).to_bytes(2, 'little')
        module_c_temp_bytes = int(self.module_c_temp).to_bytes(2, 'little')
        gate_driver_board_temp_bytes = int(
            self.gate_driver_board_temp).to_bytes(2, 'little')
        self.temperature1.data = module_a_temp_bytes + module_b_temp_bytes + \
            module_c_temp_bytes + gate_driver_board_temp_bytes

    def update_temperature2(self):
        self.control_board_temp = 240 + random() * 4.5
        self.rtd_1_temp = 230 + random() * 6.3
        self.rtd_2_temp = 225 + random() * 3.4
        self.rtd_3_temp = 220 + random() * 2.3
        control_board_temp_bytes = int(
            self.control_board_temp).to_bytes(2, 'little')
        rtd_1_temp_bytes = int(self.rtd_1_temp).to_bytes(2, 'little')
        rtd_2_temp_bytes = int(self.rtd_2_temp).to_bytes(2, 'little')
        rtd_3_temp_bytes = int(self.rtd_3_temp).to_bytes(2, 'little')
        self.temperature2.data = control_board_temp_bytes + \
            rtd_1_temp_bytes + rtd_2_temp_bytes + rtd_3_temp_bytes

    def update_temperature3(self):
        self.rtd_4_temp = 203 + random() * 2.1
        self.rtd_5_temp = 256 + random() * 3.9
        self.motor_temp = 232 + random() * 4.2
        rtd_4_temp_bytes = int(self.rtd_4_temp).to_bytes(2, 'little')
        rtd_5_temp_bytes = int(self.rtd_5_temp).to_bytes(2, 'little')
        motor_temp_bytes = int(self.motor_temp).to_bytes(2, 'little')
        # TODO once set torque value gets stored
        torque_shudder_bytes = int(0).to_bytes(2, 'little')
        self.temperature3.data = rtd_4_temp_bytes + \
            rtd_5_temp_bytes + motor_temp_bytes + torque_shudder_bytes

    def update_analog_input_voltages(self):
        self.analog_input_1 = 120 + random() * 10.4
        self.analog_input_2 = 200 + random() * 7.1
        self.analog_input_3 = 178 + random() * 2.3
        self.analog_input_4 = 153 + random() * 6.6
        analog_input_1_bytes = int(self.analog_input_1).to_bytes(2, 'little')
        analog_input_2_bytes = int(self.analog_input_2).to_bytes(2, 'little')
        analog_input_3_bytes = int(self.analog_input_3).to_bytes(2, 'little')
        analog_input_4_bytes = int(self.analog_input_4).to_bytes(2, 'little')
        self.analog_input_voltages.data = analog_input_1_bytes + \
            analog_input_2_bytes + analog_input_3_bytes + analog_input_4_bytes

    def update_digital_input_status(self):
        pass

    def update_motor_position_information(self):
        self.motor_angle = 180 + random() * 180
        self.motor_speed = (
            self.speed_command if self.speed_mode_enable else self.torque_command)
        self.electrical_output_frequency = 1000 + random() * 20
        self.delta_filter_resolved = 900 + random() * 900
        motor_angle_bytes = int(self.motor_angle).to_bytes(2, 'little')
        motor_speed_bytes = int(self.motor_speed * 10).to_bytes(2, 'little')
        electrical_output_frequency_bytes = int(
            self.electrical_output_frequency).to_bytes(2, 'little')
        delta_filter_resolved_bytes = int(
            self.delta_filter_resolved).to_bytes(2, 'little')
        self.motor_position_information.data = motor_angle_bytes + motor_speed_bytes + \
            electrical_output_frequency_bytes + delta_filter_resolved_bytes

    def update_current_information(self):
        self.phase_a_current = 20 + random() * 5
        self.phase_b_current = 20 + random() * 5
        self.phase_c_current = 20 + random() * 5
        self.dc_bus_current = 15 + random() * 6
        phase_a_current_bytes = int(self.phase_a_current).to_bytes(2, 'little')
        phase_b_current_bytes = int(self.phase_b_current).to_bytes(2, 'little')
        phase_c_current_bytes = int(self.phase_c_current).to_bytes(2, 'little')
        dc_bus_current_bytes = int(self.dc_bus_current).to_bytes(2, 'little')
        self.current_information.data = phase_a_current_bytes + \
            phase_b_current_bytes + phase_c_current_bytes + dc_bus_current_bytes

    def update_voltage_information(self):
        self.dc_bus_voltage = 200 + random() * 7.1
        self.output_voltage = 205 + random() * 5.5
        self.vab_vd_voltage = 190 + random() * 9.1
        self.vbc_vq_voltage = 180 + random() * 6.4
        dc_bus_voltage_bytes = int(self.dc_bus_voltage).to_bytes(2, 'little')
        output_voltage_bytes = int(self.output_voltage).to_bytes(2, 'little')
        vab_vd_voltage_bytes = int(self.vab_vd_voltage).to_bytes(2, 'little')
        vbc_vq_voltage_bytes = int(self.vbc_vq_voltage).to_bytes(2, 'little')
        self.voltage_information.data = dc_bus_voltage_bytes + \
            output_voltage_bytes + vab_vd_voltage_bytes + vbc_vq_voltage_bytes

    def update_flux_information(self):
        self.flux_command = 2 + random() * .64
        self.flux_feedback = 2 + random() * .64
        self.id_feedback = 20 + random() * 5
        self.iq_feedback = 20 + random() * 5
        flux_command_bytes = int(self.flux_command).to_bytes(2, 'little')
        flux_feedback_bytes = int(self.flux_feedback).to_bytes(2, 'little')
        id_feedback_bytes = int(self.id_feedback).to_bytes(2, 'little')
        iq_feedback_bytes = int(self.iq_feedback).to_bytes(2, 'little')
        self.flux_information.data = flux_command_bytes + \
            flux_feedback_bytes + id_feedback_bytes + iq_feedback_bytes

    def update_internal_voltages(self):
        self.one_five_voltage_ref = 150
        self.two_five_voltage_ref = 250
        self.five_voltage_ref = 500
        self.twelve_system_voltage = 1200
        one_five_voltage_ref_bytes = int(
            self.one_five_voltage_ref).to_bytes(2, 'little')
        two_five_voltage_ref_bytes = int(
            self.two_five_voltage_ref).to_bytes(2, 'little')
        five_voltage_ref_bytes = int(
            self.five_voltage_ref).to_bytes(2, 'little')
        twelve_system_voltage_bytes = int(
            self.twelve_system_voltage).to_bytes(2, 'little')
        self.internal_voltages.data = one_five_voltage_ref_bytes + \
            two_five_voltage_ref_bytes + five_voltage_ref_bytes + twelve_system_voltage_bytes

    def update_internal_states(self):
        pass

    def update_fault_codes(self):
        pass

    def update_torque_timer_information(self):
        self.power_on_timer = time.time() * 0.03
        commanded_torque_bytes = int(
            self.torque_command * 10).to_bytes(2, 'little')
        torque_feedback_bytes = int(
            self.torque_command * 10).to_bytes(2, 'little')
        power_on_timer_bytes = int(self.power_on_timer).to_bytes(4, 'little')
        self.torque_timer_info.data = commanded_torque_bytes + \
            torque_feedback_bytes + power_on_timer_bytes

    def update_modulation_index(self):
        pass

    def read_configuration_message(self, message: can.Message):
        BIT_1 = 1
        BIT_2 = 2
        BIT_3 = 4
        self.torque_command = int.from_bytes(
            message.data[:2], byteorder='little', signed=True) / 10
        self.speed_command = int.from_bytes(
            message.data[2:4], byteorder='little', signed=True) / 10
        self.direction_command = bool(message.data[4])
        self.inverter_enable = message.data[5] & BIT_1
        self.inverter_discharge = message.data[5] & BIT_2
        self.speed_mode_enable = message.data[5] & BIT_3
        self.commanded_torque_limit = int.from_bytes(
            message.data[6:], byteorder='little', signed=True) / 10

    def send_information_messages_10hz(self):
        time.sleep(1 / 10)
        self.can_bus.bus.send(self.temperature1)
        self.can_bus.bus.send(self.temperature2)
        self.can_bus.bus.send(self.temperature3)
        self.can_bus.bus.send(self.internal_voltages)
        self.can_bus.bus.send(self.fault_codes)

    def send_information_messages_100hz(self):
        time.sleep(1 / 100)
        self.can_bus.bus.send(self.analog_input_voltages)
        self.can_bus.bus.send(self.digital_input_status)
        self.can_bus.bus.send(self.motor_position_information)
        self.can_bus.bus.send(self.current_information)
        self.can_bus.bus.send(self.voltage_information)
        self.can_bus.bus.send(self.flux_information)
        self.can_bus.bus.send(self.internal_states)
        self.can_bus.bus.send(self.torque_timer_info)
        self.can_bus.bus.send(self.modulation_index_flux_weakening)


def run_simulation(bus_name: str):
    sim = DTSSimulator(bus_name)
    simulator_configured = False
    while simulator_configured == False:
        message = sim.can_bus.bus.recv()
        if message.arbitration_id == 192:
            sim.read_configuration_message(message)
            simulator_configured = True
    while True:
        message = sim.can_bus.bus.recv(0.1)
        sim.check_can_timeout(message)
        if message is not None and message.arbitration_id == 192:
            sim.read_configuration_message(message)
        sim.update_temperature1()
        sim.update_temperature2()
        sim.update_temperature3()
        sim.update_analog_input_voltages()
        sim.update_digital_input_status()
        sim.update_motor_position_information()
        sim.update_current_information()
        sim.update_voltage_information()
        sim.update_flux_information()
        sim.update_internal_voltages()
        sim.update_internal_states()
        sim.update_fault_codes()
        sim.update_torque_timer_information()
        sim.update_modulation_index()
        sim.send_information_messages_10hz()
        sim.send_information_messages_100hz()
        print(sim)


if __name__ == "__main__":
    run_simulation('vcan0')
