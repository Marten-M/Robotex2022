"""Helper functions for solving maze."""
from typing import Tuple


def get_relative_coords(x: int, y: int, heading: int) -> Tuple[int, int]:
    """
    Get coordinates of maze square the robot is currently facing.
    
    :param x: current x coordinate of the robot
    :param y: current y coordinate of the robot
    :param heading: heading of the robot, rounded to the closest multiple of 90 degrees

    :return: x and y coordinates of the square the robot is facing in the format (x, y)
    """
    quarter = heading % 360 // 90

    if quarter == 0: # Robot is facing north
        return x, y - 1
    elif quarter == 1: # Robot is facing east
        return x + 1, y
    elif quarter == 2: # Robot is facing south
        return x, y + 1
    else: # Robot is facing west
        return x - 1, y
