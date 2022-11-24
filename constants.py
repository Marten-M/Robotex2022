"""Constants to be used."""
# from typing import List, Tuple, Callable
from machine import Pin

# Physical constants
SOUND_SPEED_CMPS = 34300 # Speed of sound in centimeters per second

# Multipliers derived from constants
ACTUAL_DISTANCE_MULTIPLIER_CM = SOUND_SPEED_CMPS / 2 # Speed of sound divided by 2 to get distance from wall

# Constant tables
COMPARISON_OPERATORS = {
    '>': lambda a, b: a > b,
    '<': lambda a, b: a < b,
    '==': lambda a, b: a == b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '!=': lambda a, b: a != b
}

# Labyrinth constants
LABYRINTH_SQUARE_LENGTH_CM = 18 # Length of a single maze square in centimeters
LABYRINTH_WALL_THICKNESS_CM = 1.2 # Thickness of a labyrinth wall
LABYRINTH_SQUARES_HORIZONTAL = 16 # How many squares the labyrinth has horizontally
LABYRINTH_SQUARES_VERTICAL = 16 # How many squares the labyrinth has vertically

# Robot constants
ROBOT_WIDTH_CM = 10
ROBOT_LENGTH_CM = 15
ROBOT_HEIGHT_CM = 7

# Type definitions
# maze = List[List[int]] # type definition for the maze matrix
# command_list = List[Tuple[Callable, Tuple[int]]]

# Technical constants
PWM_FREQUENCY = 1000 # Frequency to set the PWM's to in Hz
MAX_U16_INT = 65535 # Maximum size of a 16bit integer (2 ^ 16 - 1)

# Motor pins
MOTOR_DRIVER_CARRIER_MODE_PIN = Pin(19, Pin.OUT)
LEFT_MOTOR_ENABLE_PIN = Pin(26, Pin.OUT)
LEFT_MOTOR_PHASE_PIN = Pin(20, Pin.OUT)
RIGHT_MOTOR_ENABLE_PIN = Pin(28, Pin.OUT)
RIGHT_MOTOR_PHASE_PIN = Pin(21, Pin.OUT)

# Gyro pins
GYRO_SCL_PIN = Pin(15)
GYRO_SDA_PIN = Pin(16)

# Ultrasonic sensors pins
LEFT_ULTRASONIC_TRIGGER_PIN = Pin(17, Pin.OUT)
LEFT_ULTRASONIC_ECHO_PIN = Pin(18, Pin.IN)
FRONT_ULTRASONIC_TRIGGER_PIN = Pin(19, Pin.OUT)
FRONT_ULTRASONIC_ECHO_PIN = Pin(20, Pin.IN)
RIGHT_ULTRASONIC_TRIGGER_PIN = Pin(21, Pin.OUT)
RIGHT_ULTRASONIC_ECHO_PIN = Pin(22, Pin.IN)
