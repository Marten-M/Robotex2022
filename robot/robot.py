"""Robot class."""
# Sensors
from sensors.gyro import GyroSensor
from sensors.ultrasonic import UltraSonicSensor
# Motors
from motors.DualMotorDriverCarriers import DualMotorDriverCarrier


class Robot(object):
    def __init__(self, motors: DualMotorDriverCarrier, gyro: GyroSensor, left_ultrasonic: UltraSonicSensor, front_ultrasonic: UltraSonicSensor, right_ultrasonic: UltraSonicSensor) -> None:
        """
        Initialize Robot class.

        :param motors: Dual motor carrier of the robot
        :param gyro: gyro sensor of the robot
        :param left_ultrasonic: left side ultrasonic sensor
        :param front_ultrasonic: front ultrasonic sensor
        :param right_ultrasonic: right side ultrasonic sensor
        """
        self.motors = motors

        self.gyro = gyro
        # Ultrasonic sensors
        self.l_us = left_ultrasonic
        self.f_us = front_ultrasonic
        self.r_us = right_ultrasonic

        # Constant variables
        self.turn_offset = 0.3 # How much the robot overturns on turning at default speed

    
    def dual_drive(self, left_motor_speed: int, right_motor_speed: int) -> None:
        """
        Set left and right motor speeds.

        :param left_motor_speed: percentage of speed to set the left motor (-100 to 100)
        :param right_motor_speed: percentage of speed to set the right motor (-100 to 100)

        :return: None
        """
        self.motors.set_left_motor_speed(left_motor_speed)
        self.motors.set_right_motor_speed(right_motor_speed)
    
    def turn(self, target_angle: int, speed: int=70) -> None:
        """
        Turn to target angle with given speed.

        NB! Might not be very accurate with current implementation.

        :param target_angle: angle to turn to
        :param speed: percentage of speed to set the motors to (1 to 100)
        """
        cur_angle = self.gyro.get_angle()
        delta = round(target_angle - cur_angle)
        if delta > 0: # Needs to turn right
            while cur_angle < target_angle:
                self.dual_drive(speed, -speed)
                cur_angle = self.gyro.get_angle()
        elif delta < 0: # Needs to turn left
            while cur_angle > target_angle:
                self.dual_drive(-speed, speed)
                cur_angle = self.gyro.get_angle()
    
    def drive(self, distance: float, speed: int, angle: int) -> None:
        """
        Drive straight at given angle and speed for given distance.

        :param distance: distance to drive in centimeters.
        :param speed: percentage of speed to drive at.
        :param angle: angle at which to drive at.

        :return: None
        """
        # TODO