from queue import PriorityQueue
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

