import sys
import time
from random import random
from enum import Enum

import can

from can_manager import CanManager

class DTSSimulator:

    def __init__(self, bus_name: str):
        # Configure bus
        self.can_bus =  CanManager(bus_name) 

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
    # TODO Store integer values in class instead of byte objects for easier printing
    def display_temps(self):
        return f'''
        Current Temperature Status:
        Module A Temperature: {self.module_a_temp / 10}
        Module B Temperature: {self.module_b_temp / 10}
        Module C Temperature: {self.module_c_temp / 10}
        Gate Driver Board Temperature: {self.gate_driver_board_temp / 10}
        Control Board Temperature: {self.control_board_temp / 10}
        RTD 1 Temperature: {self.rtd_1_temp / 10}
        RTD 2 Temperature: {self.rtd_2_temp / 10}
        RTD 3 Temperature: {self.rtd_4_temp / 10}
        RTD 4 Temperature: {self.rtd_4_temp / 10}
        RTD 5 Temperature: {self.rtd_5_temp / 10}
        Motor Temperature: {self.motor_temp / 10}
        '''

    def display_voltages(self):
        return f'''
        Current Voltage Status:
        Analog Input 1 Voltage: {self.analog_input_1 / 100}V
        Analog Input 2 Voltage: {self.analog_input_2 / 100}V
        Analog Input 3 Voltage: {self.analog_input_3 / 100}V
        Analog Input 4 Voltage: {self.analog_input_4 / 100}V
        1.5V Reference Voltage: {self.one_five_voltage_ref / 100}V
        2.5V Reference Voltage: {self.two_five_voltage_ref / 100}V
        5.0V Reference Voltage: {self.five_voltage_ref / 100}V
        12V System Voltage: {self.twelve_system_voltage / 100}V
        DC Bus Voltage: {self.dc_bus_voltage / 10}V
        Output Voltage: {self.output_voltage / 10}V
        VAB_Vd Voltage: {self.vab_vd_voltage / 10}V
        VBC_Vq Voltage: {self.vbc_vq_voltage / 10}V
        '''
    
    def display_currents(self):
        return f'''
        Current Status:
        Phase A Current: {self.phase_a_current / 10}A
        Phase B Current: {self.phase_b_current / 10}A
        Phase C Current: {self.phase_c_current / 10}A
        DC Bus Current: {self.dc_bus_current / 10}A
        Id Feedback Current: {self.id_feedback / 10}A
        Iq Feedback Current: {self.iq_feedback / 10}A
        '''

    def display_motor_info(self):
        return f'''
        Motor Position Information:
        Motor Angle: {self.motor_angle / 10}Degrees
        Motor Speed: {self.motor_speed}RPM
        Electrical Output Frequency: {self.electrical_output_frequency / 10}Hz
        Delta Filter Resolved: {self.delta_filter_resolved / 10}Degrees
        Commanded Torque: {self.torque_command / 10} Nm
        '''

    def check_can_timeout(self, message: can.Message):
        if not self.last_received_command_message:
            self.last_received_command_message = time.time()
        if message and message.arbitration_id == 192:
            if time.time() - self.last_received_command_message > .5:
                sys.exit()
            else:
                self.last_received_command_message = time.time()

    def update_temperature1(self):
        self.module_a_temp = 200 + random() * 5.0
        self.module_b_temp = 210 + random() * 4.5
        self.module_c_temp = 205 + random() * 3.7
        self.gate_driver_board_temp = 190 + random() * 6.2
        module_a_temp_bytes = int(self.module_a_temp).to_bytes(2, 'little')
        module_b_temp_bytes = int(self.module_b_temp).to_bytes(2, 'little')
        module_c_temp_bytes = int(self.module_c_temp).to_bytes(2, 'little')
        gate_driver_board_temp_bytes = int(self.gate_driver_board_temp).to_bytes(2, 'little')
        self.temperature1.data = module_a_temp_bytes + module_b_temp_bytes + \
            module_c_temp_bytes + gate_driver_board_temp_bytes

    def update_temperature2(self):
        self.control_board_temp = 240 + random() * 4.5
        self.rtd_1_temp = 230 + random() * 6.3
        self.rtd_2_temp = 225 + random() * 3.4
        self.rtd_3_temp = 220 + random() * 2.3
        control_board_temp_bytes = int(self.control_board_temp).to_bytes(2, 'little')
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
        self.motor_angle = self.direction_command
        self.motor_speed = self.speed_command if self.speed_mode_enable else self.torque_command
        self.electrical_output_frequency = 1000 + random() * 20
        self.delta_filter_resolved = 900 + random() * 900
        motor_angle_bytes = self.direction_command.to_bytes(2, 'little')
        motor_speed_bytes = (self.motor_speed).to_bytes(2, 'little')
        electrical_output_frequency_bytes = int(self.electrical_output_frequency).to_bytes(2, 'little')
        delta_filter_resolved_bytes = int(self.delta_filter_resolved).to_bytes(2, 'little')
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
        one_five_voltage_ref_bytes = int(self.one_five_voltage_ref).to_bytes(2, 'little')
        two_five_voltage_ref_bytes = int(self.two_five_voltage_ref).to_bytes(2, 'little')
        five_voltage_ref_bytes = int(self.five_voltage_ref).to_bytes(2, 'little')
        twelve_system_voltage_bytes = int(self.twelve_system_voltage).to_bytes(2, 'little')
        self.internal_voltages.data = one_five_voltage_ref_bytes + \
            two_five_voltage_ref_bytes + five_voltage_ref_bytes + twelve_system_voltage_bytes

    def update_internal_states(self):
        pass

    def update_fault_codes(self):
        pass

    def update_torque_timer_information(self):
        self.power_on_timer = time.time() * 0.03
        commanded_torque_bytes = int(self.torque_command).to_bytes(2, 'little')
        torque_feedback_bytes = int(self.torque_command).to_bytes(2, 'little')
        power_on_timer_bytes = int(self.power_on_timer).to_bytes(4, 'little')
        self.internal_states.data = commanded_torque_bytes + torque_feedback_bytes + power_on_timer_bytes

    def update_modulation_index(self):
        pass

    def read_configuration_message(self, message: can.Message):
        BIT_1 = 1
        BIT_2 = 2
        BIT_3 = 4
        self.torque_command = message.data[1] + message.data[0]
        self.speed_command = message.data[3] + message.data[2]
        self.direction_command = message.data[4]
        self.inverter_enable = message.data[5] & BIT_1
        self.inverter_discharge = message.data[5] & BIT_2
        self.speed_mode_enable = message.data[5] & BIT_3
        self.commanded_torque_limit = message.data[7] + message.data[6]

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
        message = sim.bus.recv()
        if message.arbitration_id == 192:
            sim.read_configuration_message(message)
            simulator_configured = True
    while True:
        message = sim.bus.recv(0.1)
        sim.check_can_timeout(message)
        if message.arbitration_id == 192:
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


if __name__ == "__main__":
    run_simulation('vcan0')
