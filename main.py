"""Main code to run in the competition."""
from lib.helper import get_robot, get_maze, execute_commands, set_pin_modes
from mazesolver.mazemapper import MazeMapper
import time
from constants import MAPPING_BUTTON_IN_PIN, MAPPING_BUTTON_OUT_PIN, SOLUTION_BUTTON_IN_PIN, SOLUTION_BUTTON_OUT_PIN

def main():
    # Initialize robot and maze
    robot = get_robot()
    maze = get_maze()
    set_pin_modes(1, MAPPING_BUTTON_OUT_PIN, SOLUTION_BUTTON_OUT_PIN)
    maze_mapper = MazeMapper(robot, maze, 30)
    solution_found = False
    # Wait for button press
    while True:
        if SOLUTION_BUTTON_IN_PIN.value() == 1:
            print("b")
        if MAPPING_BUTTON_IN_PIN.value() == 1:
            print("a")
            # Map the maze
            time.sleep(1)
            maze_mapper.map_maze_dfs(maze_mapper.start_x, maze_mapper.start_y, 0)
            solution_found = True
        if SOLUTION_BUTTON_IN_PIN.value() == 1:
            print("b")
        if SOLUTION_BUTTON_IN_PIN.value() == 1 and solution_found:
            # Solve the maze
            maze_solver = maze_mapper.get_maze_solver()
            commands = maze_solver.find_and_construct_optimal_path()
            time.sleep(1)
            execute_commands(commands)


if __name__ == "__main__":
    main()
    # robot = get_robot()
    # for i in range(4):
    #     robot.turn_90_degrees("right")
    #     time.sleep(1)
    # robot.turn_90_degrees("left")
    # for i in range(5):
    #     robot.drive(15, -50, 0)
