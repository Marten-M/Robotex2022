"""Main code to run in the competition."""
from lib.helper import get_robot, get_maze, execute_commands
from mazesolver.mazemapper import MazeMapper


def main():
    # Initialize robot and maze
    robot = get_robot()
    maze = get_maze()
    # Button press should be here to reset gyro to correct angle

    # Map the maze
    maze_mapper = MazeMapper(robot, maze, 70)
    # Button press should be here to start the mapping

    maze_mapper.map_maze_dfs(maze_mapper.start_x, maze_mapper.start_y)
    # Solve the maze
    maze_solver = maze_mapper.get_maze_solver()
    commands = maze_solver.find_and_construct_optimal_path()
    # Button press should be here to start the solving

    execute_commands(commands)


if __name__ == "__main__":
    main()