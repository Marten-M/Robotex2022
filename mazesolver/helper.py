"""Helper functions and classes for solving maze."""
from typing import Set, Tuple
from __future__ import annotations

from mazesolver.maze import Maze


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
    def __init__(self, x: int, y: int, parent: Node=None) -> None:
        """
        Initialize Node.

        :param x: x coordinate of the node
        :param y: y coordinate of the node
        :param parent: parent Node of this node

        :return: None
        """
        self.x = x
        self.y = y
        self.parent = parent

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


def get_possible_next_moves(x: int, y: int, maze: Maze) -> Set[Tuple[int, int]]:
    """
    Get possible next moves from given position in a given maze.

    :param x: x coordinate
    :param y: y coordinate
    :parma maze: maze where robot is in

    :return: set of moves in the form {(x, y), (x, y) ...}
    """
    moves = set()

    if x - 1 >= 0 and maze[y][x - 1] == 1:
        moves.add((x - 1, y))
    if x + 1 < maze.width and maze[y][x + 1] == 1:
        moves.add((x + 1, y))

    if y - 1 >= 0 and maze[y - 1][x] == 1:
        moves.add((x, y - 1))
    if y + 1 < maze.height and maze[y + 1][x] == 1:
        moves.add((x, y + 1))

    return moves


def reverse_linked_list(node: Node) -> Node:
    """
    Reverse the linked list (nodes) and return the first node.

    :param node: First node of the linked list to reverse
    """
    cur_node = node
    prev_node: Node = None
    next_node: Node = None

    while cur_node != None:
        next_node = cur_node.parent
        cur_node.parent = prev_node
        prev_node = cur_node
        cur_node = next_node

    return cur_node


def get_distance_to_next_square_center(distance_to_wall: float, side_length: float, forward: bool=True) -> float:
    """
    Get the distance from current position to the next squares center.

    :param distance_to_wall: robot's current distance to wall. Robot should be positioned approximately in the center of it's current square.
    :param side_length: length of a squares side in the maze in centimeters
    :param forward: whether the next square is ahead of the robot or behind the robot

    :return: distance to the next squares center.
    """
    squares_ahead = distance_to_wall // side_length
    if squares_ahead > 0: # We are not at the edge
        if forward:
            next_square_center_point_distance_from_wall = (squares_ahead - 1) * side_length + side_length / 2
            dist_to_next_square_center_point = distance_to_wall - next_square_center_point_distance_from_wall
        else:
            next_square_center_point_distance_from_wall = squares_ahead * side_length + side_length / 2
            dist_to_next_square_center_point = next_square_center_point_distance_from_wall - distance_to_wall
        return dist_to_next_square_center_point
    else:
        return 0


def get_angle_robot_must_be_at_to_reach_next_square(cur_node: Node, next_node: Node) -> int:
    """
    Get the angle the robot must be at to reach the next square, if driving forwards.

    :param cur_node: node the robot is currently at
    :param next_node: next node the robot must reach

    :return: angle at which the robot needs to be to drive forward to reach next node
    """
    delta_x = cur_node.x - next_node.x
    delta_y = cur_node.y - next_node.y
    
    if delta_x != 0: # Movement is horizontal
        if delta_x > 0: # Movement is to the west
            return 270
        else: # Movement is to the east
            return 90
    else: # Movement is vertical
        if delta_y > 0: # Movement is to the north
            return 0
        else: # Movement is to the south
            return 180


def get_distance_to_wall_from_square_center(node: Node, robot_angle: int, maze: Maze) -> float:
    """
    Get distance from a square's center to wall in the direction the robot is facing.

    :param node: the square the robot is in
    :param robot_angle: angle of the robot rounded up to a multiple of 90 degrees
    :maze: maze the robot is in

    :return: distance from the square's center the robot is in to the wall the robot is facing
    """
    x, y = node.x, node.y
    counter = 0

    while maze.width > x and maze.height > y and maze[y][x] == 1:
        counter += 1
        x, y = get_relative_coords(x, y, robot_angle)

    dist = (counter - 1) * maze.side_length + maze.side_length / 2
    return dist
