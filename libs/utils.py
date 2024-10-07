import requests

def normalize_angle(angle: int) -> int:
    normalized_angle = (angle + 180) % 360 - 180
    return normalized_angle

def send_matrix(matrix):
    res = requests.post(f"http://127.0.0.1:8801/api/v1/matrix/send?token=(token)", json = matrix)
    return res.json()