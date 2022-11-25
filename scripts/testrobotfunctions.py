"""Test robot functions."""
import sys
root_folder = sys.path[0] = "/.."
sys.path.insert(1, root_folder)

from time import sleep
from lib.helper import get_robot
from constants import LABYRINTH_SQUARE_LENGTH_CM

if __name__ == "__main__":
    robot = get_robot()

    robot.drive_until_dist_from_wall(30, 70, LABYRINTH_SQUARE_LENGTH_CM)
    sleep(10)
    robot.drive_until_dist_from_wall(60, -100, LABYRINTH_SQUARE_LENGTH_CM)
    sleep(10)
    robot.turn_90_degrees("left")
    sleep(10)
    robot.turn_90_degrees("right")
