import requests
import time

run_with_UI = False
border_value = 65
token = f"25822b31-3bc9-44ef-a4b0-228dbe6063db4088426d-cdbc-471d-bf8c-5161faaa3076"

def forward():
    if run_with_UI:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-cells/forward?token=(token)")
    else:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/forward?token=(token)")
def backward():
    if run_with_UI:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-cells/backward?token=(token)")
    else:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/backward?token=(token)")
def right():
    if run_with_UI:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-cells/right?token=(token)")
    else:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/right?token=(token)")
def left():
    if run_with_UI:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-cells/left?token=(token)")
    else:
        requests.post(f"http://127.0.0.1:8801/api/v1/robot-python/left?token=(token)")

def sensors():
    if run_with_UI:
        data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-cells/sensor-data?token=(token)").json()
    else:
        data = requests.get(f"http://127.0.0.1:8801/api/v1/robot-python/sensor-data?token=(token)").json()

    yaw = data["rotation_yaw"] if run_with_UI else data["rotation_yaw"]-90
    f = int(data["front_distance"] < border_value)
    b = int(data["back_distance"] < border_value)
    l = int(data["left_side_distance"] < border_value)
    r = int(data["right_side_distance"] < border_value)
    l45 = int(data["left_45_distance"] < border_value)
    r45 = int(data["right_45_distance"] < border_value)
    return yaw, f, b, l, r, l45, r45,

right()
right()
print(sensors())