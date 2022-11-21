"""Class for solving the maze."""
from typing import List

from robot.robot import Robot
from constants import LABYRINTH_SQUARE_LENGTH_CM, maze
from mazesolver.helper import Node, is_middle_square, get_possible_next_moves

maze = List[List[int]]


class MazeSolver(object):
    def __init__(self, robot: Robot, maze: maze, start_x: int, start_y: int) -> None:
        """
        Initialize MazeSolver class.

        MazeSolver class is used for reaching the maze's center point as efficiently (fast) as possible.

        :param robot: Robot that will solve the maze.
        :param maze: Maze in the form List[y][x], where a value of 1 means that square is accessible, 0 means it is not accessible
        :param start_x: x coordinate, where the robot starts in
        :param start_y: y coordinate, where the robot starts in

        :return: None
        """
        self.robot = robot
        self.maze = maze
        self.maze_width, self.maze_height = len(self.maze[0]), len(self.maze)

        self.optimal_path = self.find_optimal_path_bfs(start_x, start_y)
    
    def find_optimal_path_bfs(self, start_x: int, start_y: int) -> maze:
        """
        Find the optimal path to the center of the grid using breadth first search.
        
        :param start_x: x position the robot starts in
        :param start_y: y position the robot starts in

        :return: A maze with a single possible path to the center - the shortest path found
        """
        optimal_maze = [[0 for i in range(self.maze_width)] for j in range(self.maze_height)]
        visited = [[0 for i in range(self.maze_width)] for j in range(self.maze_height)]

        optimal_maze[start_y][start_x] = 1
        visited[start_y][start_x] = 1

        start_node = Node(start_x, start_y)

        queue = [start_node]
        final_node = None

        while len(queue) > 0:
            tmp_node = queue.pop()
            x, y = tmp_node.x, tmp_node.y

            if is_middle_square(tmp_node, self.maze_width, self.maze_height): # Goal reached
                final_node = tmp_node
                break

            moves = get_possible_next_moves(x, y, self.maze_width, self.maze_height, self.maze)
            for new_x, new_y in moves:
                if visited[new_y][new_x] == 0 # Node is not visited
                    new_node = Node(new_x, new_y, tmp_node)
                    queue.insert(0, new_node)
                    visited[new_y][new_x] = 1

        if final_node is None:
            return -1

        cur_node = final_node
        while cur_node != start_node:
            optimal_maze[cur_node.y][cur_node.x] = 1
            cur_node = cur_node.parent

        return optimal_maze

    def drive_optimal_path(self) -> None:
        """
        Finish the maze in the most optimal path
        """