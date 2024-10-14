import requests

def normalize_angle(angle: int) -> int:
    normalized_angle = (angle + 180) % 360 - 180
    return normalized_angle

def send_matrix(matrix):
    res = requests.post(f"http://127.0.0.1:8801/api/v1/matrix/send?token=(token)", json = matrix)
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

