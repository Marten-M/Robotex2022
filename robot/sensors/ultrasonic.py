"""Ultrasonic sensor class. Model HC-SRO4."""
import time

from machine import Pin

from constants import ACTUAL_DISTANCE_MULTIPLIER_CM


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

        :return: distance from ultrasonic sensor in centimeters
        """
        while self.echo.value() == 1: # Make sure it isnt already 1
            pass
        vals = []
        distance = 0
        for i in range(5):
            time.sleep(0.01)
            self.trigger.value(1)
            time.sleep_us(2)
            self.trigger.value(0)
            start_time = end_time = time.ticks_us()

            while self.echo.value() == 0 and start_time - end_time < 50000:
                start_time = time.ticks_us()

            while self.echo.value() == 1 and end_time - start_time < 50000:
                end_time = time.ticks_us()

            total_time = end_time - start_time

            distance = round(total_time * ACTUAL_DISTANCE_MULTIPLIER_CM, 1)
            if distance <= 1 or distance >= 300:
                distance = 0
            vals.append(distance)
        vals.sort()
        return vals[2] # Median value
