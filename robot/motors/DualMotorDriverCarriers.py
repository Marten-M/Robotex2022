"""Dual motor driver carrier class. Model DRV8835"""
from machine import Pin
from robot.helper import initialize_PWM_pin
from constants import PWM_FREQUENCY, MAX_U16_INT


class DualMotorDriverCarrier(object):
    def __init__(self, left_motor_enable_pin: Pin, left_motor_phase_pin: Pin, right_motor_enable_pin: Pin, right_motor_phase_pin: Pin, mode_pin: Pin) -> None:
        """
        Initialize DualMotorDriverCarrier class. Model DRV8835.

        :param left_motor_enable_pin: Pin for left motor enable
        :param left_motor_phase_pin: Pin for left motor phase regulator
        :param right_motor_enable_pin: Pin for right motor enable
        :param right_motor_phase_pin: Pin for right motor phase regulator

        :return: None
        """
        # Set mode pin to high
        self.mode_pin = mode_pin
        mode_pin.value(1)
        # Left motor
        self.lm_pwm = initialize_PWM_pin(left_motor_enable_pin, PWM_FREQUENCY, 0)
        self.lm_phase = left_motor_phase_pin
        self.left_motor_speed = 0
        # Right motor
        self.rm_pwm = initialize_PWM_pin(right_motor_enable_pin, PWM_FREQUENCY, 0)
        self.rm_phase = right_motor_phase_pin
        self.right_motor_speed = 0

    def set_left_motor_speed(self, speed: int) -> None:
        """
        Set speed of left motor.

        :param speed: speed to set the left motor in percentage of full speed (-100 to 100)

        :return: None
        """
        self.left_motor_speed = speed
        if speed >= 0:
            self.lm_phase.value(0)
            self.lm_pwm.duty_u16(int((speed / 100) * MAX_U16_INT))
        else:
            self.lm_phase.value(1)
            self.lm_pwm.duty_u16(int((-speed / 100) * MAX_U16_INT))

    def set_right_motor_speed(self, speed: int) -> None:
        """
        Set speed of right motor.

        :param speed: speed to set the left motor in percentage of full speed (-100 to 100)

        :return: None
        """
        self.right_motor_speed = speed
        if speed >= 0:
            self.rm_phase.value(0)
            self.rm_pwm.duty_u16(int((speed / 100) * MAX_U16_INT))
        else:
            self.rm_phase.value(1)
            self.rm_pwm.duty_u16(int((-speed / 100) * MAX_U16_INT))
