"""Constants to be used."""
import operator
from typing import List

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

# Type definitions
maze = List[List[int]] # type definition for the maze matrix