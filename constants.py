"""Constants to be used."""
import operator
from typing import List, Tuple, Callable

# Physical constants
SOUND_SPEED_CMPS = 34300 # Speed of sound in centimeters per second

# Multipliers derived from constants
ACTUAL_DISTANCE_MULTIPLIER_CM = SOUND_SPEED_CMPS / 2 # Speed of sound divided by 2 to get distance from wall

# Constant tables
COMPARISON_OPERATORS = {
    '>': operator.gt,
    '<': operator.lt,
    '==': operator.eq,
    '>=': operator.ge,
    '<=': operator.le,
    '!=': operator.ne
}

# Labyrinth constants
LABYRINTH_SQUARE_LENGTH_CM = 18 # Length of a single maze square in centimeters
LABYRINTH_WALL_THICKNESS_CM = 1.2 # Thickness of a labyrinth wall
LABYRINTH_SQUARES_HORIZONTAL = 16 # How many squares the labyrinth has horizontally
LABYRINTH_SQUARES_VERTICAL = 16 # How many squares the labyrinth has vertically


# Type definitions
maze = List[List[int]] # type definition for the maze matrix
command_list = List[Tuple[Callable, Tuple[int]]]

# Technical constants
PWM_FREQUENCY = 1000 # Frequency to set the PWM's to in Hz
MAX_U16_INT = 65535 # Maximum size of a 16bit integer (2 ^ 16 - 1)
