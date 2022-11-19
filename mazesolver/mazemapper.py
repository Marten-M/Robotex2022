"""Class for mapping the maze."""
from typing import Tuple, List
import copy

from robot.robot import Robot

class MazeMapper(object):
    def __init__(self, robot: Robot, maze_width: int, maze_height: int, maze_square_side_length_cm: int) -> None:
        """
        Initialize MazeMapper class.

        MazeMapper class is used for mapping the maze.

        :param robot: Robot, that maps the maze.
        :param maze_width: maze's width (number of squares)
        :param maze_height: maze's height (number of squares)
        :param maze_square_side_length_cm: length of a square's side in centimeters

        :return: None
        """
        self.robot = robot
        # Dimensions
        self.width = maze_width
        self.height = maze_height
        self.square_length = maze_square_side_length_cm
        # Maze matrix
        self.maze = [[0 * self.width] * self.height] # self.maze[y][x] to access a certain position, x increases to the right, y increases downwards
        self.visited = copy.deepcopy(self.maze) # Matrix for keeping track of visited squares

    def get_possible_directions(self) -> Tuple[bool, bool, bool]:
        """
        Get possible further driving directions.

        :return: Tuple of bools showing if its possible to drive in a certain direction in the order (left, straight, right)
        """
        left = straight = right = False
        left_dist, front_dist, right_dist = self.robot.measure_distances()
        
        if left_dist >= self.square_length:
            left = True
        if front_dist >= self.square_length:
            straight = True
        if right_dist >= self.square_length:
            right = True

        return left, straight, right

    def get_maze(self) -> List[List[int]]:
        """
        Get the maze.

        :return: List of list of integers (List[y][x]), where 1 means that the square is accessible and 0 means it is not accessible.
        """
        return self.maze