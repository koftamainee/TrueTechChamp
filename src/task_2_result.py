import time
import requests
import numpy as np
from queue import PriorityQueue

MOVE_TO_SLEEP = 0.2
MOVE_SLEEP = 0.2

# UTILS ------------------------------------------------------------
def normalize_angle(angle: int) -> int:
    normalized_angle = (angle + 180) % 360 - 180
    return normalized_angle


def send_matrix(matrix):
    res = requests.post(f"http://127.0.0.1:8801/api/v1/matrix/send?token=(token)", json=matrix)
    return res.json()


def reset_position():
    res = requests.post(f"http://127.0.0.1:8801/api/v1/maze/restart?token=(token)")


# move -- f, r, l, b
def calculate_point(position, move):
    yaw = normalize_angle(position[2])
    coords = position[:2]

    if yaw == 0:
        if move == "f":
            return [coords[0], coords[1] + 1]
        elif move == "r":
            return [coords[0] + 1, coords[1]]
        elif move == "l":
            return [coords[0] - 1, coords[1]]
        elif move == "b":
            return [coords[0], coords[1] - 1]

    elif yaw == 90:
        if move == "f":
            return [coords[0] + 1, coords[1]]
        elif move == "r":
            return [coords[0], coords[1] - 1]
        elif move == "l":
            return [coords[0], coords[1] + 1]
        elif move == "b":
            return [coords[0] - 1, coords[1]]

    elif yaw == -90:
        if move == "f":
            return [coords[0] - 1, coords[1]]
        elif move == "r":
            return [coords[0], coords[1] + 1]
        elif move == "l":
            return [coords[0], coords[1] - 1]
        elif move == "b":
            return [coords[0] + 1, coords[1]]

    elif abs(yaw) == 180:
        if move == "f":
            return [coords[0], coords[1] - 1]
        elif move == "r":
            return [coords[0] - 1, coords[1]]
        elif move == "l":
            return [coords[0] + 1, coords[1]]
        elif move == "b":
            return [coords[0], coords[1] + 1]


# ROBOT ------------------------------------------------------------
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


def move(position, run_with_UI, token, data, passed, finish_points, path_stack):
    if data[1] and calculate_point(position, "f") not in passed:
        if calculate_point(position, "f") not in finish_points:
            forward(position, run_with_UI, token)
        else:
            right(position, run_with_UI, token)
            right(position, run_with_UI, token)
            forward(position, run_with_UI, token)


    elif data[4] and calculate_point(position, "l") not in passed:
        if calculate_point(position, "l") not in finish_points:
            left(position, run_with_UI, token)
        else:
            right(position, run_with_UI, token)
            right(position, run_with_UI, token)
            forward(position, run_with_UI, token)

    elif data[2] and calculate_point(position, "r") not in passed:
        if calculate_point(position, "r") not in finish_points:
            right(position, run_with_UI, token)
        else:
            right(position, run_with_UI, token)
            right(position, run_with_UI, token)
            forward(position, run_with_UI, token)

    else:
        if len(path_stack) != 0:
            return True
        else:
            right(position, run_with_UI, token)
            right(position, run_with_UI, token)


def move_to(path, position, run_with_UI, token, maze, border_value):
    for direction in path:
        time.sleep(MOVE_TO_SLEEP)
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


# MAZE ------------------------------------------------------------
def show_maze(arr, type=2):
    l = len(arr)
    print("  ", end="")
    for i in range(l):
        print(i, end=(" " * (3 - len(str(i)))))
    print("\n")

    ch = lambda x: "* " if x else "  "
    for i in range(l):
        index = str(l - i - 1)
        index = index + (" " * (2 - len(str(index))))
        if type == 1:
            print(index, arr[i], index, end="\n")
        else:
            print(index, *list(map(ch, arr[i])), index, end="\n")

    print("  ", end="")
    for i in range(l):
        print(i, end=(" " * (3 - len(str(i)))))
    print("\n")


def update_maze(data, position, maze):
    print("Walls:")
    yaw = normalize_angle(position[2])
    yaw //= 90

    x = (position[0]) * 2 + 1
    y = (15 - position[1]) * 2 + 1

    wf = [1, 4, 3, 2]
    wr = [2, 1, 4, 3]
    wb = [3, 2, 1, 4]
    wl = [4, 3, 2, 1]

    if not data[wf[yaw]]:
        maze[y - 1][x] = 1
        maze[y - 1][x - 1] = 1
        maze[y - 1][x + 1] = 1
        print("wall forward")

    if not data[wb[yaw]]:
        maze[y + 1][x] = 1
        maze[y + 1][x + 1] = 1
        maze[y + 1][x - 1] = 1
        print("wall backward")

    if not data[wl[yaw]]:
        maze[y][x - 1] = 1
        maze[y + 1][x - 1] = 1
        maze[y - 1][x - 1] = 1
        print("wall left")

    if not data[wr[yaw]]:
        maze[y][x + 1] = 1
        maze[y + 1][x + 1] = 1
        maze[y - 1][x + 1] = 1
        print("wall right")

    print()


def processing_maze_data(maze):
    result_maze = [[0] * 16] * 16
    result_maze = np.array(result_maze)
    for i in range(1, 32, 2):
        for j in range(1, 32, 2):
            dt = [maze[i - 1][j], maze[i][j + 1], maze[i + 1][j], maze[i][j - 1]]
            ri = int(i / 2)
            rj = int(j / 2)
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

            result_maze[ri][rj] = res

    return result_maze


# GRAPH ------------------------------------------------------------
def update_graph(maze_graph, data, position, action):
    yaw = normalize_angle(position[2])
    coords = position[:2]

    if action == "f":
        if yaw == 0:
            coords[1] += 1
        elif yaw == 90:
            coords[0] -= 1
        elif abs(yaw) == 180:
            coords[1] -= 1
        elif yaw == -90:
            coords[0] += 1
    elif action == "r":
        if yaw == 0:
            coords[0] += 1
        elif yaw == 90:
            coords[1] -= 1
        elif abs(yaw) == 180:
            coords[0] -= 1
        elif yaw == -90:
            coords[1] += 1
    elif action == "l":
        if yaw == 0:
            coords[0] -= 1
        elif yaw == 90:
            coords[1] += 1
        elif abs(yaw) == 180:
            coords[0] += 1
        elif yaw == -90:
            coords[1] -= 1


    maze_graph[str(coords)] = []
    if yaw == 0:
        if data[1] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] + 1]))
        if data[2] == 1:
            maze_graph[str(coords)].append(str([coords[0] + 1, coords[1]]))
        if data[3] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] - 1]))
        if data[4] == 1:
            maze_graph[str(coords)].append(str([coords[0] - 1, coords[1]]))
    elif yaw == 90:
        if data[1] == 1:
            maze_graph[str(coords)].append(str([coords[0] + 1, coords[1]]))
        if data[2] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] - 1]))
        if data[3] == 1:
            maze_graph[str(coords)].append(str([coords[0] - 1, coords[1]]))
        if data[4] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] + 1]))
    elif abs(yaw) == 180:
        if data[1] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] - 1]))
        if data[2] == 1:
            maze_graph[str(coords)].append(str([coords[0] - 1, coords[1]]))
        if data[3] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] + 1]))
        if data[4] == 1:
            maze_graph[str(coords)].append(str([coords[0] + 1, coords[1]]))
    elif yaw == -90:
        if data[1] == 1:
            maze_graph[str(coords)].append(str([coords[0] - 1, coords[1]]))
        if data[2] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] + 1]))
        if data[3] == 1:
            maze_graph[str(coords)].append(str([coords[0] + 1, coords[1]]))
        if data[4] == 1:
            maze_graph[str(coords)].append(str([coords[0], coords[1] - 1]))


def parse_node(node_str):
    """Converts a string representation of a node to a tuple of integers."""
    return tuple(map(int, node_str.strip('[]').split(', ')))


def stringify_node(node_tuple):
    """Converts a tuple representation of a node back to string format."""
    return f'[{node_tuple[0]}, {node_tuple[1]}]'


def heuristic(a, b):
    # Using Manhattan distance as a base heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(graph, start, target):
    open_set = PriorityQueue()
    start_tuple = parse_node(start)  # Convert start to tuple
    target_tuple = parse_node(target)  # Convert target to tuple

    open_set.put((0, start_tuple))

    came_from = {}

    # Initialize g_score and f_score with tuples as keys
    g_score = {parse_node(node): float('inf') for node in graph}
    g_score[start_tuple] = 0

    f_score = {parse_node(node): float('inf') for node in graph}
    f_score[start_tuple] = heuristic(start_tuple, target_tuple)

    while not open_set.empty():
        current = open_set.get()[1]

        if current == target_tuple:
            return reconstruct_path(came_from, current)

        for neighbor in graph.get(stringify_node(current), []):
            neighbor_tuple = parse_node(neighbor)  # Parse neighbor to tuple

            # Ensure g_score for neighbor is initialized
            if neighbor_tuple not in g_score:
                g_score[neighbor_tuple] = float('inf')  # Initialize if not present

            # Determine the cost of the move, including turn costs
            tentative_g_score = g_score[current] + 1  # Base cost for moving

            # Check if the move involves a turn
            if current in came_from:
                previous_direction = (current[0] - came_from[current][0], current[1] - came_from[current][1])
                new_direction = (neighbor_tuple[0] - current[0], neighbor_tuple[1] - current[1])

                if previous_direction != new_direction:  # If the direction has changed, it's a turn
                    tentative_g_score += 1  # Adding a turn cost

            if tentative_g_score < g_score[neighbor_tuple]:
                # This path to neighbor is better than any previous one
                came_from[neighbor_tuple] = current
                g_score[neighbor_tuple] = tentative_g_score
                f_score[neighbor_tuple] = g_score[neighbor_tuple] + heuristic(neighbor_tuple, target_tuple)
                open_set.put((f_score[neighbor_tuple], neighbor_tuple))

    return []


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    # Convert path back to string format
    return [stringify_node(node) for node in total_path[::-1]]


def get_direction(current, next):
    x1, y1 = current
    x2, y2 = next
    if x2 > x1:
        return 90  # Moving east
    elif x2 < x1:
        return -90  # Moving west
    elif y2 > y1:
        return 0  # Moving north
    elif y2 < y1:
        return 180  # Moving south


# Function to adjust yaw angle and return the necessary command
def get_turn_command(current_yaw, target_yaw):
    diff = (target_yaw - current_yaw) % 360
    if diff == 0:
        return '', target_yaw
    elif diff == 90 or diff == -270:
        return 'r', target_yaw
    elif diff == -90 or diff == 270:
        return 'l', target_yaw
    elif diff == 180 or diff == -180:
        return 'b', target_yaw


# Main function to generate the command string
def generate_robot_commands(path, initial_yaw=0):
    path = [eval(point) for point in path]  # Convert path strings to lists
    commands = ''
    yaw = initial_yaw  # Start with the initial yaw

    for i in range(1, len(path)):
        current = path[i - 1]
        next_point = path[i]

        # Get the direction we need to move
        target_yaw = get_direction(current, next_point)

        # Adjust yaw and add turn command if necessary
        turn_command, yaw = get_turn_command(yaw, target_yaw)
        commands += turn_command

        # Move forward
        commands += 'f'

    return commands

# MAIN ------------------------------------------------------------
if __name__ == "__main__":
    token = "25822b31-3bc9-44ef-a4b0-228dbe6063db4088426d-cdbc-471d-bf8c-5161faaa3076"

    position = [0, 0, 0]
    maze_graph = {}
    finish_points = [[8, 8], [8, 7], [7, 7], [7, 8]]
    path_stack = []
    passed_forks = []
    run_with_UI = True
    run_with_UI = "cells" if run_with_UI else "python"
    maze = [[1] * 33] + [[1] + [0] * 31 + [1]] * 31 + [[1] * 33]
    maze = np.array(maze)
    passed = []
    loop = False
    cells_cnt = 3
    border_value = 65
    start_time = time.time()

    while cells_cnt != 256:
        print(f"Forks stack: {path_stack}")

        time.sleep(MOVE_SLEEP)
        data = sensors(run_with_UI, token, border_value)
        coords = position[:2]
        if coords not in passed:
            passed.append(coords)
            cells_cnt += 1

        update_graph(maze_graph, data, position, "none")

        print("------------------------")
        print(f"\nCells_cnt: {cells_cnt}")
        update_maze(data, position, maze)

        if cells_cnt == 255:
            path_stack.append("[7, 8]")
            print(f"Moving to {path_stack[-1]}...")
            move_graph = a_star(maze_graph, f"[{coords[0]}, {coords[1]}]", path_stack.pop())
            move_path = generate_robot_commands(move_graph, normalize_angle(position[2]))
            move_to(move_path, position, run_with_UI, token, maze, border_value)

        if (data[1] + data[2] + data[4]) > 1 and data[3] == 1:

            if data[1] == 1 and data[2] == 1 and data[4] == 1:
                calculated_coords = calculate_point(position, "r")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks and \
                        f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points)):
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                calculated_coords = calculate_point(position, "l")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks and \
                        f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points)):
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                calculated_coords = calculate_point(position, "f")
                if (f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points))):
                    forward(position, run_with_UI, token)
                else:
                    left(position, run_with_UI, token)

            elif data[1] == 1 and data[2] == 1 and data[4] == 0:
                calculated_coords = calculate_point(position, "r")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks and \
                        f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points)):
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                calculated_coords = calculate_point(position, "f")
                if (f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points))):
                    forward(position, run_with_UI, token)
                else:
                    right(position, run_with_UI, token)

            elif data[1] == 1 and data[2] == 0 and data[4] == 1:
                calculated_coords = calculate_point(position, "l")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks and \
                        f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points)):
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                calculated_coords = calculate_point(position, "f")
                if (f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points))):
                    forward(position, run_with_UI, token)
                else:
                    left(position, run_with_UI, token)

            elif data[1] == 0 and data[2] == 1 and data[4] == 1:
                calculated_coords = calculate_point(position, "l")
                if f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in passed_forks and \
                        f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points)):
                    path_stack.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")
                    passed_forks.append(f"[{calculated_coords[0]}, {calculated_coords[1]}]")

                calculated_coords = calculate_point(position, "r")
                if (f"[{calculated_coords[0]}, {calculated_coords[1]}]" not in list(map(str, finish_points))):
                    right(position, run_with_UI, token)
                    forward(position, run_with_UI, token)
                else:
                    left(position, run_with_UI, token)

        else:
            if (((data[1] + data[2] + data[4]) == 0) or loop) and (len(path_stack) != 0):
                loop = False
                print(f"Moving to {path_stack[-1]}...")
                move_graph = a_star(maze_graph, f"[{coords[0]}, {coords[1]}]", path_stack.pop())
                move_path = generate_robot_commands(move_graph, normalize_angle(position[2]))
                move_to(move_path, position, run_with_UI, token, maze, border_value)
            else:
                loop = move(position, run_with_UI, token, data, passed, finish_points, path_stack)


    show_maze(maze)

    move_graph = a_star(maze_graph, f"[0, 0]", f"[7, 7]")
    move_path = generate_robot_commands(move_graph, 0)
    print(f"---------- The maze was scanned for {time.time() - start_time} ----------")
    time.sleep(2)
    print("ARE YOU READY?")
    position = [0, 0, 0]
    reset_position()

    time.sleep(0.04)
    start_time = time.time()
    move_to(move_path, position, run_with_UI, token, maze, border_value)
    print(f"---------- The maze was passed for {time.time() - start_time} ----------")