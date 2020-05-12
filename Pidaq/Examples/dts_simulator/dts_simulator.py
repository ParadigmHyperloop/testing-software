from random import random
from enum import Enum

import can

class DTSStates(Enum):
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
    
    def __init__(self):
        self.temperature1 = can.Message(arbitration_id=160)
        self.temperature2 = can.Message(arbitration_id=161)
        self.temperature3 = can.Message(arbitration_id=162)
        self.analog_input_voltages = can.Message(arbitration_id=163)
        self.digital_input_status = can.Message(arbitration_id=164)
        self.motor_position_information = can.Message(arbitration_id=165)
        self.current_information = can.Message(arbitration_id=166)
        self.voltage_information = can.Message(arbitration_id=167)
        self.flux_information = can.Message(arbitration_id=168)
        self.internal_voltages = can.Message(arbitration_id=169)
        self.internal_states = can.Message(arbitration_id=170)
        self.fault_codes = can.Message(arbitration_id=171)
        self.torque_timer_info = can.Message(arbitration_id=172)
        self.modulation_index_flux_weakening = can.Message(arbitration_id=173)
        self.firmware_information = can.Message(arbitration_id=174)

    def update_temperature1(self):
        module_a_temperature = int(200 + random() * 5.0).to_bytes(2, 'big')
        module_b_temperature = int(210 + random() * 4.5).to_bytes(2, 'big')
        module_c_temperature = int(205 + random() * 3.7).to_bytes(2, 'big')
        gate_driver_board_temperature = int(190 + random() * 6.2).to_bytes(2, 'big')
        self.temperature1.data = [
            module_a_temperature,
            module_b_temperature,
            module_c_temperature,
            gate_driver_board_temperature
        ]
    
    def update_temperature2(self):
        control_board_temperature = int(240 + random() * 4.5).to_bytes(2, 'big')
        rtd_1_temperature = int(230 + random() * 6.3).to_bytes(2, 'big')
        rtd_2_temperature = int(225 + random() * 3.4).to_bytes(2, 'big')
        rtd_3_temperature = int(220 + random() * 2.3).to_bytes(2, 'big')
        self.temperature2.data = [
            control_board_temperature,
            rtd_1_temperature,
            rtd_2_temperature,
            rtd_3_temperature
        ]
    
    def update_temperature3(self):
        rtd_4_temperature = int(203 + random() * 2.1).to_bytes(2, 'big')
        rtd_5_temperature = int(256 + random() * 3.9).to_bytes(2, 'big')
        motor_temperature = int(232 + random() * 4.2).to_bytes(2, 'big')
        torque_shudder = None # TODO once set torque value gets stored
        self.temperature3.data = [
            rtd_4_temperature,
            rtd_5_temperature,
            motor_temperature,
            torque_shudder
        ]

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
