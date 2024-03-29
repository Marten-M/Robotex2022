"""Helper functions for robot."""
from machine import Pin, PWM


def initialize_PWM_pin(pwm_pin: Pin, frequency: int, duty: int) -> PWM:
    """
    Initialize a pin to be a PWM.

    :param pwm_pin: pin to initialize to PWM
    :param frequency: frequency to initialize the PWM to in Hz
    :param duty: u16 int to set duty cycle to

    :return: initialized PWM pin
    """
    pwm = PWM(pwm_pin)
    pwm.freq(frequency)
    pwm.duty_u16(duty)

    return pwm

def get_distances_to_wall(left_distance: float, right_distance: float, square_length: float) -> tuple:
    return round(left_distance % square_length, 1), round(right_distance % square_length, 1)
