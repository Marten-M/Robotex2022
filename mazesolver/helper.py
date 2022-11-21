"""Helper functions and classes for solving maze."""
from typing import Set, Tuple

from constants import maze


def get_relative_coords(x: int, y: int, heading: int) -> Tuple[int, int]:
    """
    Get coordinates of maze square the robot is currently facing.
    
    :param x: current x coordinate of the robot
    :param y: current y coordinate of the robot
    :param heading: heading of the robot, rounded to the closest multiple of 90 degrees

    :return: x and y coordinates of the square the robot is facing in the format (x, y)
    """
    quarter = heading % 360 // 90

    if quarter == 0: # Robot is facing north
        return x, y - 1
    elif quarter == 1: # Robot is facing east
        return x + 1, y
    elif quarter == 2: # Robot is facing south
        return x, y + 1
    else: # Robot is facing west
        return x - 1, y


class Node(object):
    def __init__(self, x: int, y: int, parent=None) -> None:
        """
        Initialize Node.

        :param x: x coordinate of the node
        :param y: y coordinate of the node
        :param parent: parent Node of this node

        :return: None
        """
        self.x = x
        self.y = y
        self.parent = parent if parent is not None else self

    def __ne__(self, other) -> bool:
        return not (self.x == other.x and self.y == other.y)
    



def is_middle_square(node: Node, maze_width: int, maze_height: int) -> bool:
    """
    Check whether given node is a middle square.

    :param node: node to check
    :param maze_width: width of the maze
    :param maze_height: height of the maze

    :return: boolean indicating whether the given node is a middle square
    """
    if maze_width % 2 == 0:
        x_mid = {maze_width // 2, maze_width // 2 - 1}
    else:
        x_mid = {maze_width // 2}
    
    if maze_height % 2 == 0:
        y_mid = {maze_height // 2, maze_height // 2 - 1}
    else:
        y_mid = {maze_height // 2}
    
    return node.x in x_mid and node.y in y_mid


def get_possible_next_moves(x: int, y: int, maze_width: int, maze_height: int, maze: maze) -> Set[Tuple[int, int]]:
    """
    Get possible next moves from given position in a given maze.

    :param x: x coordinate
    :param y: y coordinate
    :param maze_width: width of the maze
    :param maze_height: height of the maze
    :parma maze: maze where robot is in

    :return: set of moves in the form {(x, y), (x, y) ...}
    """
    moves = set()

    if x - 1 >= 0 and maze[y][x - 1] == 1:
        moves.add((x - 1, y))
    if x + 1 < maze_width and maze[y][x + 1] == 1:
        moves.add((x + 1, y))

    if y - 1 >= 0 and maze[y - 1][x] == 1:
        moves.add((x, y - 1))
    if y + 1 < maze_height and maze[y + 1][x] == 1:
        moves.add((x, y + 1))

    return moves