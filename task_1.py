import requests
import numpy as np
import math
import time

import os
from dotenv import load_dotenv

# angle [-inf:+inf], return normalized angle [-180:180]
def normalize_angle(angle: int) -> int:
    normalized_angle = (angle + 180) % 360 - 180
    return normalized_angle
        

def show_maze(arr, type = 2):
    l = len(arr)
    print("  ", end="")
    for i in range(l):
        print(i, end=(" " * (3 - len(str(i)))))
    print("\n")


    ch = lambda x: "* " if x else "  "
    for i in range(l):
        index = str(l-i-1)
        index = index + (" " * (2 - len(str(index))))
        if type == 1:
            print(index , arr[i], index, end="\n")
        else:
            print(index, *list(map(ch, arr[i])), index, end="\n")

    print("  ", end="")
    for i in range(l):
        print(i, end=(" " * (3 - len(str(i)))))
    print("\n")


def update_position(action):
    yaw = position[2]
    yaw = normalize_angle(yaw)
    print(f"update_position normalized yaw: {yaw}")
    if (yaw == 0 or abs(yaw) == 180):
        if action == "forward":
            position[1] += 1 if yaw == 0 else -1
        elif action == "backward":
            position[1] -= 1 if yaw == 0 else -1
    else:
        if action == "forward":
            position[0] += 1 if yaw == 90 else -1
        elif action == "backward":
            position[0] -= 1 if yaw == 90 else -1

    if action == "right":
        position[2] += 90
    elif action == "left":
        position[2] -= 90

    print(action, position)


def update_maze(data):
    yaw = normalize_angle(position[2])
    yaw //= 90

    x = (position[0])*2+1
    y = (15-position[1])*2+1
    print(f"maze position: x: {x}, y: {y}")

    wf = [1, 4, 3, 2]
    wr = [2, 1, 4, 3]
    wb = [3, 2, 1, 4]
    wl = [4, 3, 2, 1]
    # print("f r b l", position)
    # print(data[1], data[2], data[3], data[4])
    # print(data[wf[yaw]], data[wr[yaw]], data[wb[yaw]], data[wl[yaw]])
    if not(data[wf[yaw]]):
        maze[y-1][x] = 1 #set wall forward
        maze[y-1][x-1] = 1  # set wall forward
        maze[y-1][x+1] = 1  # set wall forward
        print("wall forward")
    if not(data[wb[yaw]]):
        maze[y+1][x] = 1 #set wall backward
        maze[y+1][x+1] = 1  # set wall backward
        maze[y+1][x-1] = 1  # set wall backward
        print("wall backward")
    if not(data[wl[yaw]]):
        maze[y][x-1] = 1 #set wall left
        maze[y+1][x - 1] = 1  # set wall left
        maze[y-1][x - 1] = 1  # set wall left
        print("wall left")
    if not(data[wr[yaw]]):
        maze[y][x+1] = 1 #set wall right
        maze[y+1][x + 1] = 1  # set wall right
        maze[y-1][x + 1] = 1  # set wall right
        print("wall right")

def forward():
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/forward?token=(token)")
    update_position("forward")
def backward():
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/backward?token=(token)")
    update_position("backward")
def right():
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/right?token=(token)")
    update_position("right")
def left():
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/left?token=(token)")
    update_position("left")

def restart():
    requests.post(f"http://127.0.0.1:8801/api/v1/maze/restart?token=(token)")

#TODO: реализовать отправку матрицы
def send_matrix(arr):
    res = requests.post(f"http://127.0.0.1:8801/api/v1/matrix/send?token=(token)", json = arr)
    print(res, res.status_code)

def processing_maze_data(maze):
    result_maze = [[0]*16]*16
    result_maze = np.array(result_maze)
    for i in range(1, 32, 2):
        for j in range(1, 32, 2):
            dt = [maze[i-1][j], maze[i][j+1], maze[i+1][j], maze[i][j-1]]
            ri = int(i/2)
            rj = int(j/2)
            res = -1
            if (sum(dt) == 0):
                res = 0
            elif (sum(dt) == 1 and dt[3] == 1):
                res = 1
            elif (sum(dt) == 1 and dt[0] == 1):
                res = 2
            elif (sum(dt) == 1 and dt[1] == 1):
                res = 3
            elif (sum(dt) == 1 and dt[2] == 1):
                res = 4

            elif (sum(dt) == 2 and dt[2] == 1 and dt[3] == 1):
                res = 5
            elif (sum(dt) == 2 and dt[2] == 1 and dt[1] == 1):
                res = 6
            elif (sum(dt) == 2 and dt[0] == 1 and dt[1] == 1):
                res = 7
            elif (sum(dt) == 2 and dt[0] == 1 and dt[3] == 1):
                res = 8

            elif (sum(dt) == 2 and dt[3] == 1 and dt[1] == 1):
                res = 9
            elif (sum(dt) == 2 and dt[0] == 1 and dt[2] == 1):
                res = 10

            elif (sum(dt) == 3 and dt[3] == 0):
                res = 11
            elif (sum(dt) == 3 and dt[2] == 0):
                res = 12
            elif (sum(dt) == 3 and dt[1] == 0):
                res = 13
            elif (sum(dt) == 3 and dt[0] == 0):
                res = 14

            elif (sum(dt) == 4):
                res = 15

            #print(i, j, ri, rj, res)
            result_maze[ri][rj] = res

    return result_maze


# data[1] -- forward
# data[2] -- right 
# data[3] -- backwards 
# data[4] -- left
def move_to(path: str) -> None:
    time.sleep(0.04)
    for direction in path:
        if direction == "f":
            forward()
        elif direction == "l":
            left()
            forward()
        elif direction == "r":
            right()
            forward()
        else:
            right()
            right()


def sensors():
    if run_with_UI == "cells":
        data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-cells/sensor-data?token=(token)").json()
    else:
        data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-python/sensor-data?token=(token)").json()

    yaw = data["rotation_yaw"] if (run_with_UI == "cells") else data["rotation_yaw"]-90
    #position[2] = yaw
    f = int(data["front_distance"] > border_value)
    b = int(data["back_distance"] > border_value)
    l = int(data["left_side_distance"] > border_value)
    r = int(data["right_side_distance"] > border_value)
    l45 = int(data["left_45_distance"] > border_value)
    r45 = int(data["right_45_distance"] > border_value)
    return yaw, f, r, b, l #l45, r45


# data[1] -- forward
# data[2] -- right 
# data[3] -- backwards 
# data[4] -- left
def move() -> str:
    direction = ""
    if data[1]:
        forward()
    elif data[4]:
        left()
        forward()
    elif data[2]:
        right()
        forward()
    else:
        right()
        right()
    return direction


if __name__ == "__main__":
    # put your token to TRUETECH_TOKEN in .env
    load_dotenv()
    token = os.getenv("TRUETECH_TOKEN")

    #run_with_UI = check_simulator()
    cnt = 0
    prev_coords = [-1, -1]
    border_value = 65
    run_with_UI = True
    run_with_UI = "cells" if run_with_UI else "python"
    #restart()
    position = [0,0,0]
    maze = [[1]*33] + [[1] + [0]*31 + [1]]*31 + [[1]*33]
    maze = np.array(maze)

    #while (True):
    print("yaw, f, b, l, r, l45, r45")
    passed = []
    cells_cnt = 0
    #for i in range(50):
    while (cells_cnt != 256):

        # max speed for unix systems
        time.sleep(0.04)

        print("--------------")
        data = sensors()
        coords = position[:2]
        print()
        print(f"Position: {coords}, cells_cnt = {cells_cnt}")
        print()
        if cells_cnt == 0:
            print(position)
        if coords not in passed:
            passed.append(coords)
            cells_cnt += 1
            
            print("--------------")

        update_maze(data)
        print(data, end=" ")
        print(cells_cnt)
        

        if (data[1] + data[2] + data[4]) > 1:
            if data[1] == 1 and [coords[0], coords[1] + 1] not in passed:
                move_to("f")
            elif data[2] == 1 and [coords[0] + 1, coords[1]] not in passed:
                move_to("r")
            elif data[4] == 1 and [coords[0] - 1, coords[1]] not in passed:
                move_to("l")
            else:
                move()

        else:
            move()

        if prev_coords == coords:
            cnt += 1
        prev_coords = coords
        if cnt > 30:
            break
        # input()

    show_maze(maze)
    print(position)
    result = processing_maze_data(maze)
    result = result.tolist()
    print(result)
    send_matrix(result)
