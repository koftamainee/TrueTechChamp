import time
from libs.utils import normalize_angle, calculate_point
from libs.maze import update_maze
import libs.API

import sys


class MouseCrashedError(Exception):
    pass

def command(args, return_type=None):
    line = " ".join([str(x) for x in args]) + "\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    if return_type:
        response = sys.stdin.readline().strip()
        if return_type == bool:
            return response == "true"
        return return_type(response)

def mazeWidth():
    return command(args=["mazeWidth"], return_type=int)

def mazeHeight():
    return command(args=["mazeHeight"], return_type=int)

def checkWall(wallCommand, half_steps_away=None):
    args = [wallCommand]
    if half_steps_away is not None:
        args.append(half_steps_away)
    return command(args, return_type=bool)

def wallFront(half_steps_away=None):
    return checkWall("wallFront", half_steps_away)

def wallBack(half_steps_away=None):
    return checkWall("wallBack", half_steps_away)

def wallLeft(half_steps_away=None):
    return checkWall("wallLeft", half_steps_away)

def wallRight(half_steps_away=None):
    return checkWall("wallRight", half_steps_away)

def wallFrontLeft(half_steps_away=None):
    return checkWall("wallFrontLeft", half_steps_away)

def wallFrontRight(half_steps_away=None):
    return checkWall("wallFrontRight", half_steps_away)

def wallBackLeft(half_steps_away=None):
    return checkWall("wallBackLeft", half_steps_away)

def wallBackRight(half_steps_away=None):
    return checkWall("wallBackRight", half_steps_away)

def moveForward(distance=None):
    args = ["moveForward"]
    # Don't append distance argument unless explicitly specified, for
    # backwards compatibility with older versions of the simulator
    if distance is not None:
        args.append(distance)
    response = command(args=args, return_type=str)
    if response == "crash":
        raise MouseCrashedError()

def moveForwardHalf(num_half_steps=None):
    args = ["moveForwardHalf"]
    if num_half_steps is not None:
        args.append(num_half_steps)
    response = command(args=args, return_type=str)
    if response == "crash":
        raise MouseCrashedError()

def turnRight():
    command(args=["turnRight"], return_type=str)

def turnLeft():
    command(args=["turnLeft"], return_type=str)

def turnRight90():
    turnRight()

def turnLeft90():
    turnLeft()

def turnRight45():
    command(args=["turnRight45"], return_type=str)

def turnLeft45():
    command(args=["turnLeft45"], return_type=str)

def setWall(x, y, direction):
    command(args=["setWall", x, y, direction])

def clearWall(x, y, direction):
    command(args=["clearWall", x, y, direction])

def setColor(x, y, color):
    command(args=["setColor", x, y, color])

def clearColor(x, y):
    command(args=["clearColor", x, y])

def clearAllColor():
    command(args=["clearAllColor"])

def setText(x, y, text):
    command(args=["setText", x, y, text])

def clearText(x, y):
    command(args=["clearText", x, y])

def clearAllText():
    command(args=["clearAllText"])

def wasReset():
    return command(args=["wasReset"], return_type=bool)

def ackReset():
    command(args=["ackReset"], return_type=str)


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
    moveForward(1)
    #requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/forward?token=(token)")
    update_position("forward", position)

def backward(position, run_with_UI, token):
    moveBackrward(1)
    #requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/backward?token=(token)")
    update_position("backward", position)

def right(position, run_with_UI, token):
    turnRight90()
    #requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/right?token=(token)")
    update_position("right", position)

def left(position, run_with_UI, token):
    turnLeft90()
    #requests.post(f"http://127.0.0.1:8801/api/v1/robot-" + run_with_UI + "/left?token=(token)")
    update_position("left", position)


def sensors(run_with_UI, token, border_value):
    # if run_with_UI == "cells":
    #     data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-cells/sensor-data?token=(token)").json()
    # else:
    #     data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-python/sensor-data?token=(token)").json()
    # if "dict_keys(['detail'])" == str(data.keys()):
    #     print("Robot not found. Exit code 1.")
    #     exit(1)
    # # Mocked sensors logic here
    # yaw = data["rotation_yaw"] - 90
    # f = int(data["front_distance"] > border_value)
    # b = int(data["back_distance"] > border_value)
    # l = int(data["left_side_distance"] > border_value)
    # r = int(data["right_side_distance"] > border_value)
    yaw = 0
    f = 0 if wallFront() else 1
    r = 0 if wallRight() else 1
    b = 0 if wallBack() else 1
    l = 0 if wallLeft() else 1
    print(yaw, f, r, b, l)
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
