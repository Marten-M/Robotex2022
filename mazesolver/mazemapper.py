"""Class for mapping the maze."""
from mazesolver.mazerunner import MazeRunner
from robot.robot import Robot
from mazesolver.helper import get_relative_coords
from mazesolver.maze import Maze


class MazeMapper(MazeRunner):
    def __init__(self, robot: Robot, maze: Maze, exploration_speed: int) -> None:
        """
        Initialize MazeMapper class.

        MazeMapper class is used for mapping the maze.

        :param robot: Robot that will solve the maze
        :param maze: Maze the robot will be in
        :param exploration_speed: how fast the robot will explore the maze (1 to 100)

        :return: None
        """
        super().__init__(robot, maze)
        # Maze matrix
        self.visited = self.maze.get_new_maze(False) # Matrix for keeping track of visited squares

        # How fast to explore the maze.
        self.exploration_speed = exploration_speed
 
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
                self.drive_to_next_square_center(self.exploration_speed)
                # Start mapping maze
                self.map_maze_dfs(new_x, new_y)
                # Return to original position
                self.drive_to_next_square_center(-self.exploration_speed)
                self.robot.turn(closest_heading)

        if straight_possible:
            new_x, new_y = get_relative_coords(x, y, closest_heading)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.drive_to_next_square_center(self.exploration_speed)
                # Map maze
                self.map_maze_dfs(new_x, new_y)
                # Return to original position
                self.drive_to_next_square_center(-self.exploration_speed)

        if right_possible:
            new_angle = 0 if closest_heading == 270 else closest_heading + 90
            new_x, new_y = get_relative_coords(x, y, new_angle)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.robot.turn(new_angle)
                self.drive_to_next_square_center(self.exploration_speed)
                # Map maze
                self.map_maze_dfs(new_x, new_y)
                # Return to original position
                self.drive_to_next_square_center(-self.exploration_speed)
                self.robot.turn(closest_heading)
