"""General helper functions"""
from machine import Pin

from robot.robot import Robot
from mazesolver.maze import Maze
from robot.motors.DualMotorDriverCarriers import DualMotorDriverCarrier
#from robot.sensors.gyro import GyroSensor
from robot.sensors.ultrasonic import UltraSonicSensor
from constants import *


def set_pin_modes(mode: int, *pins: Pin) -> None:
    """
    Set given pins to a given value.

    :param mode: 0 if pin will be set to low, 1 if high
    :param pins: all pins to set to high
    """
    for pin in pins:
        pin.value(mode)


def get_robot() -> Robot:
    """
    Get a robot with values given in constants.py

    :return: a robot with parameters specifid in constants file
    """
    dmdc = DualMotorDriverCarrier(LEFT_MOTOR_ENABLE_PIN, LEFT_MOTOR_PHASE_PIN, RIGHT_MOTOR_ENABLE_PIN, RIGHT_MOTOR_PHASE_PIN, MOTOR_DRIVER_CARRIER_MODE_PIN)
    
    #gyro = GyroSensor(GYRO_SCL_PIN, GYRO_SDA_PIN)
    gyro = None
    l_us = UltraSonicSensor(LEFT_ULTRASONIC_TRIGGER_PIN, LEFT_ULTRASONIC_ECHO_PIN)
    f_us = UltraSonicSensor(FRONT_ULTRASONIC_TRIGGER_PIN, FRONT_ULTRASONIC_ECHO_PIN)
    r_us = UltraSonicSensor(RIGHT_ULTRASONIC_TRIGGER_PIN, RIGHT_ULTRASONIC_ECHO_PIN)

    robot = Robot(dmdc, gyro, l_us, f_us, r_us, ROBOT_WIDTH_CM, ROBOT_LENGTH_CM, ROBOT_HEIGHT_CM)
    return robot


def get_maze() -> Maze:
    """
    Get a maze with values given in constants.py

    :return: a maze with specified size and initial values set to 0
    """
    return Maze(LABYRINTH_SQUARES_HORIZONTAL, LABYRINTH_SQUARES_VERTICAL, LABYRINTH_SQUARE_LENGTH_CM, 0)


def execute_commands(commands) -> None:
    """
    Execute given commands.

    :param commands: list of commands
    
    :return: None
    """
    for command, parameters in commands:
        command(*parameters)
