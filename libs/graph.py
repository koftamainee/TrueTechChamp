from collections import deque
from libs.utils import normalize_angle

def update_graph(maze_graph, data, position):
    coords = position[:2]
    maze_graph[str(coords)] = []
    yaw = normalize_angle(position[2])
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
        



def bfs(graph, start, target):
    queue = deque([[start]])
    visited = set([start])
    
    while queue:
        path = queue.popleft()
        
        node = path[-1]
        
        if node == target:
            return path 

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                visited.add(neighbor)
    

    return []

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
        current = path[i-1]
        next_point = path[i]
        
        # Get the direction we need to move
        target_yaw = get_direction(current, next_point)
        
        # Adjust yaw and add turn command if necessary
        turn_command, yaw = get_turn_command(yaw, target_yaw)
        commands += turn_command
        
        # Move forward
        commands += 'f'

    return commands

