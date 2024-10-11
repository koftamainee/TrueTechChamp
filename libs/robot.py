import requests
import time
from libs.utils import normalize_angle, calculate_point
from libs.maze import update_maze

def update_position(action, position):
    yaw = position[2]
    yaw = normalize_angle(yaw)

    if yaw == 0 or abs(yaw) == 180:
        if action == "forward":
            position[1] += (1 if yaw == 0 else -1)
        elif action == "backward":
            position[1] -= (1 if yaw == 0 else -1)
    elif abs(yaw) == 90:
        if action == "forward":
            position[0] += (1 if yaw == 90 else -1)
        elif action == "backward":
            position[0] -= (1 if yaw == 90 else -1)

    if action == "right":
        position[2] += 90
    elif action == "left":
        position[2] -= 90

    print(f"Movement: {action}, position: {position[:2]}, normalized yaw: {yaw}")

def forward(position, run_with_UI, token):
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/forward?token=(token)")
    update_position("forward", position)

def backward(position, run_with_UI, token):
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/backward?token=(token)")
    update_position("backward", position)

def right(position, run_with_UI, token):
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/right?token=(token)")
    update_position("right", position)

def left(position, run_with_UI, token):
    requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/left?token=(token)")
    update_position("left", position)


def sensors(run_with_UI, token, border_value):
    if run_with_UI == "cells":
        data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-cells/sensor-data?token=(token)").json()
    else:
        data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-python/sensor-data?token=(token)").json()
    if "dict_keys(['detail'])" == str(data.keys()):
        print("Robot not found. Exit code 1.")
        exit(1)
    # Mocked sensors logic here
    yaw = data["rotation_yaw"] - 90
    f = int(data["front_distance"] > border_value)
    b = int(data["back_distance"] > border_value)
    l = int(data["left_side_distance"] > border_value)
    r = int(data["right_side_distance"] > border_value)
    return yaw, f, r, b, l

def move(position, run_with_UI, token, data, passed):
    if data[1] and calculate_point(position, "f") not in passed:
        forward(position, run_with_UI, token)
    elif data[4] and calculate_point(position, "l") not in passed:
        left(position, run_with_UI, token)
    elif data[2] and calculate_point(position, "r") not in passed:
        right(position, run_with_UI, token)
    else:
        return True

def move_to(path, position, run_with_UI, token, maze, border_value):
    for direction in path:
        time.sleep(0.04)
        if direction == "f":
            forward(position, run_with_UI, token)
        elif direction == "r":
            right(position, run_with_UI, token)
        elif direction == "l":
            left(position, run_with_UI, token)
        elif direction == "b":
            right(position, run_with_UI, token)
            right(position, run_with_UI, token)
    
        data = sensors(run_with_UI, token, border_value)
