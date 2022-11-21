"""Class for mapping the maze."""
from typing import Tuple

from robot.robot import Robot
from mazesolver.helper import get_relative_coords

from constants import LABYRINTH_SQUARE_LENGTH_CM, maze


class MazeMapper(object):
    def __init__(self, robot: Robot, maze_width: int, maze_height: int) -> None:
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
        self.square_length = LABYRINTH_SQUARE_LENGTH_CM
        # Maze matrix
        self.maze = [[0 for i in range(self.width)] for j in range(self.height)] # self.maze[y][x] to access a certain position, x increases to the right, y increases downwards
        self.visited = [[False for i in range(self.width)] for j in range(self.height)] # Matrix for keeping track of visited squares

        # How fast to explore the maze.
        self.exploration_speed = 50

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

    def get_maze(self) -> maze:
        """
        Get the maze.

        :return: List of list of integers (List[y][x]), where 1 means that the square is accessible and 0 means it is not accessible.
        """
        return self.maze
 
    def map_maze_dfs(self, x: int, y: int) -> None:
        """
        Map the maze using depth first search.

        Does not check behind itself - when mapping maze place it in a corner of the maze.

        :param x: current x coordinate
        :param y: current y coordinate

        :return: None
        """
        self.visited[y][x] = True

        left_possible, straight_possible, right_possible = self.get_possible_directions()
        closest_heading = self.robot.get_closest_90_degree_heading()


        if left_possible:
            new_angle = 270 if closest_heading == 0 else closest_heading - 90
            new_x, new_y = get_relative_coords(x, y, new_angle)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.robot.turn(new_angle)
                self.robot.drive(self.square_length, self.exploration_speed, new_angle)
                # Start mapping maze
                self.map_maze_dfs(new_x, new_y)
                # Return to original position
                self.robot.drive(self.square_length, -self.exploration_speed, new_angle)
                self.robot.turn(closest_heading)

        if straight_possible:
            new_x, new_y = get_relative_coords(x, y, closest_heading)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.robot.drive(self.square_length, self.exploration_speed, closest_heading)
                # Map maze
                self.map_maze_dfs(new_x, new_y)
                # Return to original position
                self.robot.drive(self.square_length, -self.exploration_speed, closest_heading)

        if right_possible:
            new_angle = 0 if closest_heading == 270 else closest_heading + 90
            new_x, new_y = get_relative_coords(x, y, new_angle)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.robot.turn(new_angle)
                self.robot.drive(self.square_length, self.exploration_speed, new_angle)
                # Map maze
                self.map_maze_dfs(new_x, new_y)
                # Return to original position
                self.robot.drive(self.square_length, -self.exploration_speed, new_angle)
                self.robot.turn(closest_heading)
