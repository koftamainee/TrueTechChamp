from queue import PriorityQueue

def parse_node(node_str):
    """Converts a string representation of a node to a tuple of integers."""
    return tuple(map(int, node_str.strip('[]').split(', ')))

def stringify_node(node_tuple):
    """Converts a tuple representation of a node back to string format."""
    return f'[{node_tuple[0]}, {node_tuple[1]}]'

def heuristic(a, b):
    # Using Manhattan distance as a base heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_with_turns(graph, start, target):
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

# Example usage
graph = {
    '[0, 0]': ['[1, 0]'], 
    '[1, 0]': ['[2, 0]', '[0, 0]'],
    '[2, 0]': ['[3, 0]', '[1, 0]'],
    '[3, 0]': ['[3, 1]', '[2, 0]'],
    '[3, 1]': ['[3, 2]', '[2, 1]', '[3, 0]'],
    '[3, 2]': ['[4, 2]', '[3, 1]'],
    '[4, 2]': ['[5, 2]', '[3, 2]'],
    '[5, 2]': ['[6, 2]', '[4, 2]'],
    '[6, 2]': ['[7, 2]', '[5, 2]'],
    '[7, 2]': ['[7, 1]', '[6, 2]'],
    '[7, 1]': ['[7, 0]', '[6, 1]', '[7, 2]'],
    '[7, 0]': ['[7, 1]', '[6, 0]'],
    '[6, 1]': ['[6, 2]', '[7, 1]'],
    '[6, 0]': ['[7, 0]', '[5, 0]'],
    '[5, 0]': ['[6, 0]', '[4, 0]'],
    '[4, 0]': ['[5, 0]', '[3, 0]'],
    '[3, 1]': ['[3, 0]', '[2, 1]'],
    '[2, 1]': ['[2, 2]', '[1, 1]', '[3, 1]'],
    '[1, 1]': ['[1, 2]', '[0, 1]', '[2, 1]'],
    '[0, 1]': ['[0, 0]', '[1, 1]'],
    '[1, 2]': ['[2, 2]', '[1, 1]', '[0, 2]'],
    '[2, 2]': ['[2, 1]', '[3, 2]', '[1, 2]'],
}

start = '[0, 0]'
target = '[1, 2]'
path = a_star_with_turns(graph, start, target)
print("Path with fewer turns:", path)
