"""Robot class."""
from typing import Tuple
# Sensors
from robot.sensors.gyro import GyroSensor
from robot.sensors.ultrasonic import UltraSonicSensor
# Motors
from robot.motors.DualMotorDriverCarriers import DualMotorDriverCarrier

from constants import COMPARISON_OPERATORS

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
        self.turn_offset = 0 # How much the robot overturns on turning at default speed, use for this not yet implemented
        self.braking_distance = 0 # How long the braking distance is when driving at full speed.

    def dual_drive(self, left_motor_speed: int, right_motor_speed: int) -> None:
        """
        Set left and right motor speeds.

        :param left_motor_speed: percentage of speed to set the left motor (-100 to 100)
        :param right_motor_speed: percentage of speed to set the right motor (-100 to 100)

        :return: None
        """
        self.motors.set_left_motor_speed(left_motor_speed)
        self.motors.set_right_motor_speed(right_motor_speed)

    def brake(self) -> None:
        """
        Stop the motors.

        :return: None
        """
        self.motors.set_left_motor_speed(0)
        self.motors.set_right_motor_speed(0)

    def turn_until(self, left_motor_speed: int, right_motor_speed: int, angle: int, cmp_to_current_angle: str='>', brake: bool=False) -> None:
        """
        Turn the robot until a condition is no longer met.

        :param left_motor_speed: speed at which to turn the left motor
        :param right_motor_speed: speed at which to turn the right motor
        :param angle: angle to compare with current angle
        :param cmp_to_current_angle: what operation to use when comparing (">", "<", ">=", "<=", "==", "!=")
        :param brake: whether to brake at the end or not.

        :return: None
        """
        cur_angle = self.gyro.get_angle()

        while COMPARISON_OPERATORS[cmp_to_current_angle](angle, cur_angle):
            self.dual_drive(left_motor_speed, right_motor_speed)
            cur_angle = self.gyro.get_angle()

        if brake:
            self.brake()

    def turn(self, target_angle: int, speed: int=70) -> None:
        """
        Turn to target angle with given speed.

        NB! Might not be very accurate with current implementation.

        :param target_angle: angle to turn to
        :param speed: percentage of speed to set the motors to (1 to 100)
        """
        cur_angle = self.gyro.get_angle()

        if target_angle > cur_angle:
            right_degrees = target_angle - cur_angle
            left_degrees = cur_angle + (360 - target_angle)
        else:
            right_degrees = (360 - cur_angle) + target_angle
            left_degrees = cur_angle - target_angle
        
        if right_degrees > left_degrees: # Turn left
            if target_angle > cur_angle:
                self.turn_until(-speed, speed, target_angle, '>')
            
            self.turn_until(-speed, speed, target_angle, '<')
        else: # Turn right
            if target_angle < cur_angle:
                self.turn_until(speed, -speed, target_angle, '<')
            
            self.turn_until(speed, -speed, target_angle, '>')

        self.brake()

    def drive(self, distance: float, speed: int, angle: int) -> None:
        """
        Drive straight at given angle and speed for given distance.

        Make sure robot starts at the correct angle, or the distance wont be calculated correctly

        :param distance: distance to drive in centimeters.
        :param speed: percentage of speed to drive at.
        :param angle: angle at which to drive at. - NOT CURRENTLY IMPLEMENTED

        :return: None
        """
        start_dist = cur_dist = self.f_us.measure_distance()
        if speed > 0:
            end_dist = start_dist - distance
            while cur_dist > end_dist - self.braking_distance:
                self.dual_drive(speed, speed)
                cur_dist = self.f_us.measure_distance()
        else:
            end_dist = start_dist + distance
            while cur_dist < end_dist - self.braking_distance:
                self.dual_drive(speed, speed)
                cur_dist = self.f_us.measure_distance()

        self.brake()

    def measure_distances(self) -> Tuple[float, float, float]:
        """
        Measure distances from all ultrasonic sensors.

        :return: Tuple of floats containing the measured distances of the robot's three ultrasonic sensors in the order (left, front, right)
        """
        left_distance = self.l_us.measure_distance()
        front_distance = self.f_us.measure_distance()
        right_distance = self.r_us.measure_distance()

        return left_distance, front_distance, right_distance

    def get_closest_90_degree_heading(self) -> int:
        """
        Get the closest multiple of 90 degrees the robot is heading towards.

        :return: Closest multiple of 90 of the current robot's angle.
        """
        cur_angle = round(self.gyro.get_angle())
        multiplier = cur_angle // 90
        point1, point2 = multiplier * 90, (multiplier + 1) * 90

        if abs(point1 - cur_angle) > abs(point2 - cur_angle):
            return point2
        else:
            return point1
