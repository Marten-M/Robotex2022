"""Test robot functions."""
import sys
import os
root_folder = os.path.join(sys.path[0], "..")
sys.path.insert(1, root_folder)

from time import sleep
from lib.helper import get_robot

if __name__ == "__main__":
    robot = get_robot()

    robot.drive(100, 70, 0)
    sleep(10)
    robot.drive_until_dist_from_wall(30, 70)
    sleep(10)
    robot.drive_until_dist_from_wall(60, -100)
    sleep(10)
    robot.turn(90)
