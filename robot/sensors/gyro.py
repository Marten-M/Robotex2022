"""Gyro sensor class. Model GY-273 HMC5883L."""
from machine import Pin

from lib.hmc5883l import HMC5883L


class GyroSensor(object):
    def __init__(self, scl: Pin, sda: Pin) -> None:
        """
        Initialize GyroSensor class. Model GY-273 HMC5883L.

        :param scl: Pin for serial clock
        :param sda: Pin for serial data

        :return: None
        """
        self.sensor = HMC5883L(scl, sda)
        self.offset = 0
    
    def get_heading(self) -> float:
        """
        Get heading of the robot in degrees.

        :return: Heading of the robot with accuracy up to 0.1 degrees
        """
        x, y, z = self.sensor.read()
        degrees, minutes = self.sensor.heading(x, y)
        return round(degrees + minutes / 60, 1)

    def reset_angle(self, angle: float) -> None:
        """
        Reset angle of gyro sensor to given value.

        :param angle: angle to reset the gyro sensor to.

        :return: None
        """
        self.offset = self.get_heading() - round(angle, 1)

    def get_angle(self) -> float:
        """
        Get angle of the robot in degrees.

        :return: Angle of the robot with accuracy up to 0.1 degrees
        """
        return round((360 + self.get_heading() - self.offset) % 360, 1)
