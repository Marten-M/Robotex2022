"""Class for the robot solving the maze."""
from robot.robot import Robot

from mazesolver.helper import get_distance_to_next_square_center
from mazesolver.maze import Maze
from constants import LABYRINTH_SQUARE_LENGTH_CM
import time


class MazeRunner(object):
    def __init__(self, robot: Robot, maze: Maze, start_x: int=0) -> None:
        """
        Initialize MazeRunner class.

        :param robot: Robot that will solve the maze.
        :param start_x: x coordinate the robot will start in

        :return: None
        """
        self.robot = robot

        self.maze = maze
        self.start_x = start_x
        self.start_y = self.maze.height - 1 # Robot always starts at the bottom of the maze

    def get_possible_directions(self) -> tuple:
        """
        Get possible further driving directions.

        :return: Tuple of bools showing if its possible to drive in a certain direction in the order (left, straight, right)
        """
        left = straight = right = False
        left_dist, front_dist, right_dist = self.robot.measure_distances()

        if left_dist >= self.maze.side_length:
            left = True
        if front_dist >= self.maze.side_length:
            straight = True
        if right_dist >= self.maze.side_length:
            right = True

        return left, straight, right
    
    def drive_to_next_square_center(self, speed: int, brake: bool=True) -> None:
        """
        Drive to the center of the next square.

        :param speed: speed at which to drive at (-100 to 100)
        :param brake: whether to brake in the end

        :return: None
        """
        dist_to_wall = self.robot.f_us.measure_distance()
        if speed > 0:
        #     # dist = dist_to_wall - get_distance_to_next_square_center(dist_to_wall, self.maze.side_length, forward=True) - self.robot.length / 2
            dist = get_distance_to_next_square_center(dist_to_wall, self.maze.side_length, forward=True) + self.robot.length / 2
        else:
        #     # dist = dist_to_wall + get_distance_to_next_square_center(dist_to_wall, self.maze.side_length, forward=False) + self.robot.length / 2
            dist = get_distance_to_next_square_center(dist_to_wall, self.maze.side_length, forward=False) - self.robot.length / 2
        # self.robot.drive_until_dist_from_wall(dist, speed, self.maze.side_length, brake)
        self.robot.drive(dist, speed, 0)
        time.sleep(0.3)
