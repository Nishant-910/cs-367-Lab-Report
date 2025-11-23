from collections import deque

class PuzzleNode:
    def __init__(self, config, parent=None):
        self.config = config
        self.parent = parent

def expand(node_obj):
    children = []
    empty_index = node_obj.config.index(0)
    moves = [-1, 1, 3, -3]  # left, right, down, up (for 3x3 puzzle)

    for shift in moves:
        new_idx = empty_index + shift
        if 0 <= new_idx < 9:
            new_state = list(node_obj.config)
            new_state[empty_index], new_state[new_idx] = new_state[new_idx], new_state[empty_index]
            children.append(PuzzleNode(new_state, node_obj))
    return children

def breadth_first(start_config, goal_config):
    start_node = PuzzleNode(start_config)
    goal_node = PuzzleNode(goal_config)

    frontier = deque([start_node])
    visited = set()
    explored_count = 0

    while frontier:
        current = frontier.popleft()
        if tuple(current.config) in visited:
            continue
        visited.add(tuple(current.config))

        print(current.config)
        explored_count += 1

        if current.config == goal_node.config:
            path = []
            while current:
                path.append(current.config)
                current = current.parent
            print("Nodes explored:", explored_count)
            return path[::-1]

        for child in expand(current):
            frontier.append(child)

    print("Nodes explored:", explored_count)
    return None

initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
target_state  = [1, 2, 3, 4, 5, 6, 0, 7, 8]

result = breadth_first(initial_state, target_state)

if result:
    print("Solution path:")
    for step in result:
        print(step)
else:
    print("No solution found.")