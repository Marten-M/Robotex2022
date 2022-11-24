"""Class for the robot solving the maze."""
from robot.robot import Robot

from mazesolver.helper import get_distance_to_next_square_center
from mazesolver.maze import Maze


class MazeRunner(object):
    def __init__(self, robot: Robot, maze: Maze) -> None:
        """
        Initialize MazeRunner class.

        :param robot: Robot that will solve the maze.

        :return: None
        """
        self.robot = robot

        self.maze = maze
    
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
            dist = dist_to_wall - get_distance_to_next_square_center(dist_to_wall, self.maze.side_length, forward=True)
        else:
            dist = dist_to_wall + get_distance_to_next_square_center(dist_to_wall, self.maze.side_length, forward=False)
        self.robot.drive_until_dist_from_wall(dist, speed, brake)
