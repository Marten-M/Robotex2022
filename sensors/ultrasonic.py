"""Ultrasonic sensor class. Model HC-SRO4."""
import time

from machine import Pin

from constants import GET_ACTUAL_DISTANCE_MULTIPLIER_CM


class UltraSonicSensor(object):
    def __init__(self, trigger: Pin, echo: Pin) -> None:
        """
        Initialize UltraSonicSensor class. Model HC-SRO4.

        :param trigger: Pin class for trigger pin
        :param echo: Pin class for echo pin

        :return: None
        """
        self.trigger = trigger
        self.echo = echo

    def measure_distance(self) -> float:
        """
        Measure distance in centimeters.

        :return: None
        """
        while self.echo.value() == 1: # Make sure it isnt already 1
            pass

        distance = 0

        self.trigger.value(1)
        end_time = time.time()
        start_time = time.time()

        while self.echo.value() == 0:
            end_time = time.time()
        
        total_time = end_time - start_time

        distance = total_time * GET_ACTUAL_DISTANCE_MULTIPLIER_CM

        return distance