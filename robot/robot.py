"""Robot class."""
import time, math
# Sensors
from robot.sensors.gyro import GyroSensor
from robot.sensors.ultrasonic import UltraSonicSensor
# Motors
from robot.motors.DualMotorDriverCarriers import DualMotorDriverCarrier

from robot.helper import get_distances_to_wall
from constants import COMPARISON_OPERATORS

class Robot(object):
    def __init__(self, motors: DualMotorDriverCarrier, gyro: GyroSensor, left_ultrasonic: UltraSonicSensor, front_ultrasonic: UltraSonicSensor, right_ultrasonic: UltraSonicSensor, width: float, length: float, height: float) -> None:
        """
        Initialize Robot class.

        :param motors: Dual motor carrier of the robot
        :param gyro: gyro sensor of the robot
        :param left_ultrasonic: left side ultrasonic sensor
        :param front_ultrasonic: front ultrasonic sensor
        :param right_ultrasonic: right side ultrasonic sensor
        :param width: width of the robot in centimeters
        :param length: length of the robot in centimeters
        :param height: height of the robot in centimeters
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
        self.dist_inaccuracy = 0.2 # How accurately the ultrasonic sensor must detect a distance to turn accurately
        # Robot dimensions
        self.width = width
        self.length = length
        self.height = height

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

    def turn_until(self, left_motor_speed: int, right_motor_speed: int, angle: int, cmp_to_current_angle: str='>') -> None:
        """
        Turn the robot until a condition is no longer met.

        :param left_motor_speed: speed at which to turn the left motor
        :param right_motor_speed: speed at which to turn the right motor
        :param angle: angle to compare with current angle
        :param cmp_to_current_angle: what operation to use when comparing (">", "<", ">=", "<=", "==", "!=")

        :return: None
        """
        cur_angle = self.gyro.get_angle()

        self.dual_drive(left_motor_speed, right_motor_speed)
        while COMPARISON_OPERATORS[cmp_to_current_angle](angle, cur_angle):
            cur_angle = self.gyro.get_angle()

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

    def turn_90_degrees(self, direction: str):
        if direction == "right":
            r_dist = self.r_us.measure_distance()
            f_dist = self.f_us.measure_distance()
            self.dual_drive(70, -70)
            time.sleep_ms(200)
            while r_dist + self.dist_inaccuracy < f_dist:
                f_dist = self.f_us.measure_distance()
        else:
            l_dist = self.l_us.measure_distance()
            f_dist = self.f_us.measure_distance()
            self.dual_drive(-70, 70)
            time.sleep_ms(200)
            while l_dist + self.dist_inaccuracy < f_dist:
                f_dist = self.f_us.measure_distance()

        self.brake()

    def drive(self, distance: float, speed: int, angle: int, brake: bool=True) -> None:
        """
        Drive straight at given angle and speed for given distance.

        Make sure robot starts at the correct angle, or the distance wont be calculated correctly

        :param distance: distance to drive in centimeters.
        :param speed: percentage of speed to drive at.
        :param angle: angle at which to drive at. - NOT CURRENTLY IMPLEMENTED
        :param brake: whether to brake or not

        :return: None
        """
        start_dist = cur_dist = self.f_us.measure_distance()
        if speed > 0:
            end_dist = start_dist - distance
            self.dual_drive(speed, speed)
            while cur_dist > end_dist + self.braking_distance:
                cur_dist = self.f_us.measure_distance()
        else:
            end_dist = start_dist + distance
            self.dual_drive(speed, speed)
            while cur_dist < end_dist - self.braking_distance:
                cur_dist = self.f_us.measure_distance()

        if brake:
            self.brake()

    def drive_until_dist_from_wall(self, distance: float, speed: int, square_length: float, brake: bool=True) -> None:
        """
        Drive until the robot reaches a certain distance from the wall.

        :param distance: distance to reach from the wall the robot is facing in centimeters
        :param speed: speed at which the robot should drive at (-100 to 100)
        :param brake: whether to brake at the end

        :return: None
        """
        cur_reading = self.f_us.measure_distance()
        if speed > 0:
            self.dual_drive(speed, speed)
            while cur_reading - self.braking_distance > distance:
                left_dist, cur_reading, right_dist = self.measure_distances()
                left_dist, right_dist = get_distances_to_wall(left_dist, right_dist, square_length)
                if left_dist > right_dist:
                    self.dual_drive(speed - math.ceil((left_dist - right_dist)) * 2, speed)
                elif right_dist > left_dist:
                    self.dual_drive(speed, speed - math.ceil(right_dist - left_dist) * 2)
        else:
            self.dual_drive(speed, speed)
            while cur_reading + self.braking_distance < distance:
                left_dist, cur_reading, right_dist = self.measure_distances()
                left_dist, right_dist = get_distances_to_wall(left_dist, right_dist, square_length)
                if left_dist > right_dist:
                    self.dual_drive(speed + math.ceil((left_dist - right_dist)) * 2, speed)
                elif right_dist > left_dist:
                    self.dual_drive(speed, speed + math.ceil(right_dist - left_dist) * 2)

        if brake:
            self.brake()

    def measure_distances(self) -> tuple:
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
