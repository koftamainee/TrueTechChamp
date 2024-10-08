import os
import time
import requests
import numpy as np
from dotenv import load_dotenv
from libs.robot import forward, backward, right, left, sensors, move, move_to
from libs.maze import update_maze, show_maze, processing_maze_data
from libs.utils import normalize_angle, send_matrix, calculate_point
from libs.graph import update_graph, bfs, generate_robot_commands


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TRUETECH_TOKEN")

    position = [0, 0, 0]
    maze_graph = {}
    path_stack = []
    passed_forks = []
    run_with_UI = True
    run_with_UI = "cells" if run_with_UI else "python"
    maze = [[1] * 33] + [[1] + [0] * 31 + [1]] * 31 + [[1] * 33]
    maze = np.array(maze)
    passed = []
    cells_cnt = 0
    border_value = 65

    while cells_cnt != 256:

        time.sleep(0.04)
        data = sensors(run_with_UI, token, border_value)
        coords = position[:2]
        if coords not in passed:
            passed.append(coords)
            cells_cnt += 1
        
        
        update_graph(maze_graph, data, position)
        
        print("------------------------")
        print(f"\nCells_cnt: {cells_cnt}")
        update_maze(data, position, maze)

        if (data[1] + data[2] + data[4]) > 1:

            if data[1] == 1 and data[2] == 1 and data[3] == 1:
                calculated_coords = calculate_point(position, "r")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks:
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                calculated_coords = calculate_point(position, "l")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks:
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                forward(position, run_with_UI, token)

            elif data[1] == 1 and data[2] == 1 and data[3] == 0:
                calculated_coords = calculate_point(position, "r")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks:
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                
                forward(position, run_with_UI, token)

            elif data[1] == 1 and data[2] == 0 and data[3] == 1:
                calculated_coords = calculate_point(position, "l")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks:
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                
                forward(position, run_with_UI, token)

            elif data[1] == 0 and data[2] == 1 and data[3] == 1:
                calculated_coords = calculate_point(position, "l")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks:
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                
                right(position, run_with_UI, token)
                forward(position, run_with_UI, token)
            
        else:
            if (data[1] + data[2] + data[4]) == 0:
                move_graph = bfs(maze_graph, f"[{coords[0]}, {coords[1]}]", path_stack.pop())
                move_path = generate_robot_commands(move_graph, normalize_angle(position[2]))
                move_to(move_path, position, run_with_UI, token, maze, border_value)
            else:
                move(position, run_with_UI, token, data)

        

    show_maze(maze)
    matrix = processing_maze_data(maze)
    matrix = matrix.tolist()
    print(f"Answer matrix: {matrix}")
    res = send_matrix(matrix)
    print()

    print("Score:", res["Score"], "/ 256")
    