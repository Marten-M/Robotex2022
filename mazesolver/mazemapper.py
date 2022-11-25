"""Class for mapping the maze."""
from mazesolver.mazerunner import MazeRunner
from mazesolver.mazesolver import MazeSolver
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

        self.horizontal_pos_found = False

    def map_maze_dfs(self, x: int, y: int, angle: int) -> None:
        """
        Map the maze using depth first search.

        Does not check behind itself - when mapping maze place it in a corner of the maze.

        :param x: current x coordinate
        :param y: current y coordinate
        :param angle: angle at which the robot is at

        :return: None
        """
        self.visited[y][x] = True

        left_possible, straight_possible, right_possible = self.get_possible_directions()

        if not self.horizontal_pos_found and (left_possible or right_possible): # Horizontal position found
            self.horizontal_pos_found = True
            if left_possible: # Robot started in the right side of the maze
                x = self.maze.width - 1

                tmp_y = y
                while tmp_y < self.maze.height: # Correct the maze mapping
                    self.visited[tmp_y][0] = False
                    self.maze[tmp_y][0] = 0

                    self.visited[tmp_y][x] = True
                    self.maze[tmp_y][x] = 1

                    tmp_y += 1

        if left_possible:
            new_angle = 270 if angle == 0 else angle - 90
            new_x, new_y = get_relative_coords(x, y, new_angle)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.robot.turn_90_degrees("left")
                self.drive_to_next_square_center(self.exploration_speed)
                # Start mapping maze
                self.map_maze_dfs(new_x, new_y, new_angle)
                # Return to original position
                self.drive_to_next_square_center(-self.exploration_speed)
                self.robot.turn_90_degrees("right")

        if straight_possible:
            new_x, new_y = get_relative_coords(x, y, angle)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.drive_to_next_square_center(self.exploration_speed)
                # Map maze
                self.map_maze_dfs(new_x, new_y, angle)
                # Return to original position
                self.drive_to_next_square_center(-self.exploration_speed)

        if right_possible:
            new_angle = 0 if angle == 270 else angle + 90
            new_x, new_y = get_relative_coords(x, y, new_angle)
            self.maze[new_y][new_x] = 1

            if not self.visited[new_y][new_x]:
                # Head to next square
                self.robot.turn_90_degrees("right")
                self.drive_to_next_square_center(self.exploration_speed)
                # Map maze
                self.map_maze_dfs(new_x, new_y, new_angle)
                # Return to original position
                self.drive_to_next_square_center(-self.exploration_speed)
                self.robot.turn_90_degrees("left")

    def get_maze_solver(self) -> MazeSolver:
        """
        Get a maze solver based on mapped maze.

        :return: a maze solver class based on mapped maze.
        """
        solver = MazeSolver(self.robot, self.maze)
        solver.start_x = self.start_x
        solver.start_y = self.start_y

        return solver