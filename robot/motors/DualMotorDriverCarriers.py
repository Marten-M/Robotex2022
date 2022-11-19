"""Dual motor driver carrier class. Model DRV8835"""
from machine import Pin, PWM


class DualMotorDriverCarrier(object):
    def __init__(self, left_motor_enable_pin: Pin, left_motor_phase_pin: Pin, right_motor_enable_pin: Pin, right_motor_phase_pin: Pin) -> None:
        """
        Initialize DualMotorDriverCarrier class. Model DRV8835.

        :param left_motor_enable_pin: Pin for left motor enable
        :param left_motor_phase_pin: Pin for left motor phase regulator
        :param right_motor_enable_pin: Pin for right motor enable
        :param right_motor_phase_pin: Pin for right motor phase regulator

        :return: None
        """
        # Left motor
        self.lm_pwm = PWM(left_motor_enable_pin)
        self.lm_pwm.freq(0)
        self.lm_phase = left_motor_phase_pin
        # Right motor
        self.rm_pwm = PWM(right_motor_enable_pin)
        self.rm_pwm.freq(0)
        self.rm_phase = right_motor_phase_pin

    def set_left_motor_speed(self, speed: int) -> None:
        """
        Set speed of left motor.

        :param speed: speed to set the left motor in percentage of full speed (-100 to 100)

        :return: None
        """
        if speed >= 0:
            self.lm_phase.value(0)
            self.lm_pwm.freq(speed)
        else:
            self.lm_phase.value(1)
            self.lm_pwm.freq(-speed)

    def set_right_motor_speed(self, speed: int) -> None:
        """
        Set speed of right motor.

        :param speed: speed to set the left motor in percentage of full speed (-100 to 100)

        :return: None
        """
        if speed >= 0:
            self.rm_phase.value(1)
            self.rm_pwm.freq(speed)
        else:
            self.rm_phase.value(0)
            self.rm_pwm.freq(-speed)
