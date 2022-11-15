"""Dual motor driver carrier class. Model DRV8835"""
from machine import Pin


class DualMotorDriverCarrier(object):
    def __init__(self, left_motor_power_pin: Pin, left_motor_phase_pin: Pin, right_motor_power_pin: Pin, right_motor_phase_pin: Pin) -> None:
        """
        Initialize DualMotorDriverCarrier class. Model DRV8835.

        :param left_motor_power_pin: Pin for left motor power
        :param left_motor_phase_pin: Pin for left motor phase regulator
        :param right_motor_power_pin: Pin for right motor power
        :param right_motor_phase_pin: Pin for right motor phase regulator

        :return: None
        """
        # Left motor
        self.lm_power = left_motor_power_pin
        self.lm_phase = left_motor_phase_pin
        # Right motor
        self.rm_power = right_motor_power_pin
        self.rm_phase = right_motor_phase_pin

    
    