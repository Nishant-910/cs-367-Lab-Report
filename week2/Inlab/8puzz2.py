import heapq

class PuzzleNode:
    def __init__(self, config, parent=None, g_cost=0, h_cost=0):
        self.config = config
        self.parent = parent
        self.g = g_cost
        self.h = h_cost
        self.f = g_cost + h_cost

    def __lt__(self, other):
        return self.f < other.f

def heuristic_manhattan(state, target):
    total = 0
    for val in range(1, 9):
        x1, y1 = divmod(state.index(val), 3)
        x2, y2 = divmod(target.index(val), 3)
        total += abs(x1 - x2) + abs(y1 - y2)
    return total

def expand(node_obj, goal):
    children = []
    blank = node_obj.config.index(0)
    moves = [-1, 1, 3, -3]  # left, right, down, up (relative shifts)
    for shift in moves:
        pos = blank + shift
        if 0 <= pos < 9:
            new_cfg = list(node_obj.config)
            new_cfg[blank], new_cfg[pos] = new_cfg[pos], new_cfg[blank]
            g_new = node_obj.g + 1
            h_new = heuristic_manhattan(new_cfg, goal)
            children.append(PuzzleNode(new_cfg, node_obj, g_new, h_new))
    return children

def astar_solver(start_cfg, goal_cfg):
    start_node = PuzzleNode(start_cfg, None, 0, heuristic_manhattan(start_cfg, goal_cfg))
    goal_node = PuzzleNode(goal_cfg)

    frontier = []
    heapq.heappush(frontier, start_node)
    explored = set()
    explored_count = 0

    while frontier:
        current = heapq.heappop(frontier)

        if tuple(current.config) in explored:
            continue
        explored.add(tuple(current.config))
        explored_count += 1

        if current.config == goal_node.config:
            path = []
            while current:
                path.append(current.config)
                current = current.parent
            print("Nodes explored (A*):", explored_count)
            return path[::-1]

        for child in expand(current, goal_cfg):
            if tuple(child.config) not in explored:
                heapq.heappush(frontier, child)

    print("Nodes explored (A*):", explored_count)
    return None

initial_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
target_state  = [1, 2, 3, 4, 5, 6, 0, 7, 8]

solution = astar_solver(initial_state, target_state)

if solution:
    print("Solution path:")
    for step in solution:
        print(step)
else:
    print("No solution found.")