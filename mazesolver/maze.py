"""Class for the maze."""
from __future__ import annotations


class Maze(object):
    def __init__(self, width: int, height: int, side_length: int, default_val) -> None:
        """
        Initialize Maze.

        :param width: width of the maze
        :param height: height of the maze
        :param side_length: length of a side of a square of the maze in centimeters
        :param default_val: default value to fill the maze with

        :return: None
        """
        self.width = width
        self.height = height
        self.side_length = side_length

        self.maze = [[default_val for i in range(width)] for j in range(height)]
    
    def __getitem__(self, index: int) -> list:
        return self.maze[index]
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Maze):
            return self.maze == __o.maze
        return False

    def get_new_maze(self, default_val) -> Maze:
        """
        Get a new Maze object with exact same properties but with a customly filled value

        :param default_val: value to fill the maze with initially

        :return: Maze object with this maze's properties and a new default value.
        """
        return Maze(self.width, self.height, self.side_length, default_val)
