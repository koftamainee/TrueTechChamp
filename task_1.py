import os
import time
import requests
import numpy as np
from dotenv import load_dotenv
from libs.robot import forward, backward, right, left, sensors, move
from libs.maze import update_maze, show_maze, processing_maze_data
from libs.utils import normalize_angle, send_matrix


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TRUETECH_TOKEN")

    position = [0, 0, 0]
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
        
        print("------------------------")
        print(f"\nCells_cnt: {cells_cnt}")
        update_maze(data, position, maze)

        if (data[1] + data[2] + data[4]) > 1:
            if data[1] and [coords[0], coords[1] + 1] not in passed:
                forward(position, run_with_UI, token)
            elif data[2] and [coords[0] + 1, coords[1]] not in passed:
                right(position, run_with_UI, token)
                forward(position, run_with_UI, token)
            elif data[4] and [coords[0] - 1, coords[1]] not in passed:
                left(position, run_with_UI, token)
                forward(position, run_with_UI, token)
            else:
                break
        else:
            move(position, run_with_UI, token, data)

    show_maze(maze)
    matrix = processing_maze_data(maze)
    matrix = matrix.tolist()
    print(f"Answer matrix: {matrix}")
    res = send_matrix(matrix)
    print()
    print("Score:", res["Score"], "/ 256")
    