import time
from random import random
from enum import Enum

import can


class DTSState(Enum):
    START_STATE = 0
    PRE_CHARGE_INITIAL = 1
    PRE_CHARGE_ACTIVE = 2
    PRE_CHARGE_FINISH = 3
    WAIT = 4
    READY = 5
    MOTOR_RUNNING = 6
    FAULT = 7
    RECYCLE_POWER = 65535


class DTSSimulator:

    def __init__(self, bus_name: str):

        # Configure bus
        self.bus = can.interfaces.socketcan.SocketcanBus(bus_name)

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

    def update_temperature1(self):
        module_a_temperature = int(200 + random() * 5.0).to_bytes(2, 'big')
        module_b_temperature = int(210 + random() * 4.5).to_bytes(2, 'big')
        module_c_temperature = int(205 + random() * 3.7).to_bytes(2, 'big')
        gate_driver_board_temperature = int(
            190 + random() * 6.2).to_bytes(2, 'big')
        self.temperature1.data = module_a_temperature + module_b_temperature + \
            module_c_temperature + gate_driver_board_temperature

    def update_temperature2(self):
        control_board_temperature = int(
            240 + random() * 4.5).to_bytes(2, 'big')
        rtd_1_temperature = int(230 + random() * 6.3).to_bytes(2, 'big')
        rtd_2_temperature = int(225 + random() * 3.4).to_bytes(2, 'big')
        rtd_3_temperature = int(220 + random() * 2.3).to_bytes(2, 'big')
        self.temperature2.data = control_board_temperature + \
            rtd_1_temperature + rtd_2_temperature + rtd_3_temperature

    def update_temperature3(self):
        rtd_4_temperature = int(203 + random() * 2.1).to_bytes(2, 'big')
        rtd_5_temperature = int(256 + random() * 3.9).to_bytes(2, 'big')
        motor_temperature = int(232 + random() * 4.2).to_bytes(2, 'big')
        # TODO once set torque value gets stored
        torque_shudder = int(0).to_bytes(2, 'big')
        self.temperature3.data = rtd_4_temperature + \
            rtd_5_temperature + motor_temperature + torque_shudder

    def update_analog_input_values(self):
        analog_input_1 = int(120 + random() * 10.4).to_bytes(2, 'big')
        analog_input_2 = int(200 + random() * 7.1).to_bytes(2, 'big')
        analog_input_3 = int(178 + random() * 2.3).to_bytes(2, 'big')
        analog_input_4 = int(153 + random() * 6.6).to_bytes(2, 'big')
        self.analog_input_voltages.data = [
            analog_input_1,
            analog_input_2,
            analog_input_3,
            analog_input_4
        ]

    def update_digital_input_status(self):
        pass  # This will need to read from the state

    def update_motor_position_information(self):
        motor_angle = None
        # TODO Research conversion from torque to RPM for motor
        motor_speed = (
            self.speed_command if self.speed_mode_enable else self.torque_command).to_bytes(2, 'big')
        electrical_output_frequency = None
        delta_filter_resolved = None
        self.motor_position_information = [
            motor_angle,
            motor_speed,
            electrical_output_frequency,
            delta_filter_resolved
        ]

    def update_current_information(self):
        phase_a_current = int(20 + random() * 5).to_bytes(2, 'big')
        phase_b_current = int(20 + random() * 5).to_bytes(2, 'big')
        phase_c_current = int(20 + random() * 5).to_bytes(2, 'big')
        dc_bus_current = int(15 + random() * 6).to_bytes(2, 'big')
        self.current_information = [
            phase_a_current,
            phase_b_current,
            phase_c_current,
            dc_bus_current
        ]

    def update_voltage_information(self):
        dc_bus_voltage = int(200 + random() * 7.1).to_bytes(2, 'big')
        output_voltage = int(205 + random() * 5.5).to_bytes(2, 'big')
        vab_vd_voltage = int(190 + random() * 9.1).to_bytes(2, 'big')
        vbc_vq_voltage = int(180 + random() * 6.4).to_bytes(2, 'big')
        self.voltage_information = [
            dc_bus_voltage,
            output_voltage,
            vab_vd_voltage,
            vbc_vq_voltage
        ]

    def update_flux_information(self):
        flux_command = int(2 + random() * .64).to_bytes(2, 'big')
        flux_feedback = int(2 + random() * .64).to_bytes(2, 'big')
        id_feedback = int(20 + random() * 5).to_bytes(2, 'big')
        iq_feedback = int(20 + random() * 5).to_bytes(2, 'big')
        self.flux_information = [
            flux_command,
            flux_feedback,
            id_feedback,
            iq_feedback
        ]

    def update_internal_voltages(self):
        one_five_voltage_ref = int(150).to_bytes(2, 'big')
        two_five_voltage_ref = int(250).to_bytes(2, 'big')
        five_voltage_ref = int(500).to_bytes(2, 'big')
        twelve_system_voltage = int(1200).to_bytes(2, 'big')
        self.internal_voltages = [
            one_five_voltage_ref,
            two_five_voltage_ref,
            five_voltage_ref,
            twelve_system_voltage
        ]

    def update_internal_states(self):
        pass  # Read from input configuration

    def update_fault_codes(self):
        pass

    def update_torque_timer_information(self):
        pass  # Read from command message

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
        self.bus.send(self.temperature1)
        self.bus.send(self.temperature2)
        self.bus.send(self.temperature3)
        # self.bus.send(self.internal_voltages)
        # self.bus.send(self.fault_codes)

    def send_information_messages_100hz(self):
        time.sleep(1 / 100)
        self.bus.send(self.analog_input_voltages)
        self.bus.send(self.digital_input_status)
        self.bus.send(self.motor_position_information)
        self.bus.send(self.current_information)
        self.bus.send(self.voltage_information)
        self.bus.send(self.flux_information)
        self.bus.send(self.internal_states)
        self.bus.send(self.torque_timer_info)
        self.bus.send(self.modulation_index_flux_weakening)


if __name__ == "__main__":
    sim = DTSSimulator('vcan0')
    simulator_configured = False
    while simulator_configured == False:
        message = sim.bus.recv()
        if message.arbitration_id == 192:
            sim.read_configuration_message(message)
            simulator_configured = True

    while True:
        sim.update_temperature1()
        sim.update_temperature2()
        sim.update_temperature3()
        # sim.update_analog_input_voltages()
        sim.update_digital_input_status()
        sim.update_motor_position_information()
        sim.update_current_information()
        sim.update_voltage_information()
        sim.update_flux_information()
        sim.update_internal_voltages()
        sim.update_internal_states()
        sim.update_torque_timer_information()
        sim.update_modulation_index()
        sim.send_information_messages_10hz()
