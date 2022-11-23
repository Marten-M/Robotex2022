"""Class for solving the maze."""
from robot.robot import Robot
from constants import command_list
from mazesolver.helper import Node, is_middle_square, get_possible_next_moves, get_angle_robot_must_be_at_to_reach_next_square, get_distance_to_wall_from_square_center
from mazesolver.mazerunner import MazeRunner
from mazesolver.maze import Maze


class MazeSolver(MazeRunner):
    def __init__(self, robot: Robot, maze: Maze, start_x: int, start_y: int) -> None:
        """
        Initialize MazeSolver class.

        MazeSolver class is used for reaching the maze's center point as efficiently (fast) as possible.

        :param robot: Robot that will solve the maze.
        :param maze: Maze in the form List[y][x], where a value of 1 means that square is accessible, 0 means it is not accessible
        :param start_x: x coordinate, where the robot starts in
        :param start_y: y coordinate, where the robot starts in

        :return: None
        """
        super().__init__(robot, maze)

        optimal_path = self.find_optimal_path_bfs(start_x, start_y)
    
    def find_optimal_path_bfs(self, start_x: int, start_y: int) -> Node:
        """
        Find the optimal path to the center of the grid using breadth first search.
        
        :param start_x: x position the robot starts in
        :param start_y: y position the robot starts in

        :return: A maze with a single possible path to the center - the shortest path found
        """
        visited = self.maze.get_new_maze(0)
        visited[start_y][start_x] = 1

        start_node = Node(start_x, start_y)
        queue = [start_node]
        final_node = None

        while len(queue) > 0:
            tmp_node = queue.pop()
            x, y = tmp_node.x, tmp_node.y

            if is_middle_square(tmp_node, self.maze.width, self.maze.height): # Goal reached
                final_node = tmp_node
                break

            moves = get_possible_next_moves(x, y, self.maze)
            for new_x, new_y in moves:
                if visited[new_y][new_x] == 0: # Node is not visited
                    new_node = Node(new_x, new_y, tmp_node)
                    queue.insert(0, new_node)
                    visited[new_y][new_x] = 1

        if final_node is None:
            return None

        return final_node

    def construct_optimal_path(self, start_node: Node) -> command_list:
        """
        Finish the maze in the most optimal path.

        :param start_x: x coordinate to start from
        :param start_y: y coordinate to start from

        :return: List of commands to execute to drive the optimal path in the format [(function, (param1, param2, ...)), ...]
        """
        commands = []

        cur_angle = get_angle_robot_must_be_at_to_reach_next_square(start_node, start_node.parent)

        # Initialize gyro sensor
        cmd = (self.robot.gyro.reset_angle, (cur_angle,))
        commands.append(cmd)

        cur_node = start_node

        while cur_node.parent != None:
            next_node = cur_node.parent
            new_angle = get_angle_robot_must_be_at_to_reach_next_square(cur_node, next_node)

            if cur_angle != new_angle: # Turn must be made
                # Drive to the current point
                dist_from_wall = get_distance_to_wall_from_square_center(cur_node, cur_angle, self.maze)
                cmd = (self.robot.drive_until_dist_from_wall, (dist_from_wall, 100))
                commands.append(cmd)

                cmd = (self.robot.turn, (new_angle, 100)) # Turn to angle
                commands.append(cmd)
                cur_angle = new_angle
        # Final drive
        dist_from_wall = get_distance_to_wall_from_square_center(cur_node, cur_angle, self.maze)
        cmd = (self.robot.drive_until_dist_from_wall, (dist_from_wall, 100))
        commands.append(cmd)

        return commands
