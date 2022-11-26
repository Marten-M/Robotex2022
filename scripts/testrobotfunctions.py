"""Test robot functions."""
import sys
root_folder = sys.path[0] = "/.."
sys.path.insert(1, root_folder)
from time import sleep
from lib.helper import get_robot
from constants import LABYRINTH_SQUARE_LENGTH_CM

if __name__ == "__main__":
    robot = get_robot()
    robot.dual_drive(50, 55)
    sleep(1)
    robot.brake()
