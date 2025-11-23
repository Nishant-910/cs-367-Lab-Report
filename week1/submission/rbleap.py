from collections import deque

def generate_moves(config):
    moves_list = []
    for pos in range(7):
        if config[pos] == 1:  # right mover
            if pos + 1 < 7 and config[pos + 1] == 0:
                new_cfg = list(config)
                new_cfg[pos], new_cfg[pos + 1] = 0, 1
                moves_list.append(tuple(new_cfg))
            if pos + 2 < 7 and config[pos + 2] == 0:
                new_cfg = list(config)
                new_cfg[pos], new_cfg[pos + 2] = 0, 1
                moves_list.append(tuple(new_cfg))
        elif config[pos] == -1:  # left mover
            if pos - 1 >= 0 and config[pos - 1] == 0:
                new_cfg = list(config)
                new_cfg[pos], new_cfg[pos - 1] = 0, -1
                moves_list.append(tuple(new_cfg))
            if pos - 2 >= 0 and config[pos - 2] == 0:
                new_cfg = list(config)
                new_cfg[pos], new_cfg[pos - 2] = 0, -1
                moves_list.append(tuple(new_cfg))
    return moves_list

def depth_first(initial, goal):
    stack = [(initial, [])]
    seen = set()

    while stack:
        current, path = stack.pop()

        if current in seen:
            continue
        seen.add(current)

        path = path + [current]
        if current == goal:
            print("Nodes visited (DFS):", len(seen))
            return path

        for nxt in generate_moves(current):
            stack.append((nxt, path))
    return None

def breadth_first(initial, goal):
    queue = deque([(initial, [])])
    seen = set()

    while queue:
        current, path = queue.popleft()

        if current in seen:
            continue
        seen.add(current)

        path = path + [current]
        if current == goal:
            print("Nodes visited (BFS):", len(seen))
            return path

        for nxt in generate_moves(current):
            queue.append((nxt, path))
    return None

initial_setup = (1, 1, 1, 0, -1, -1, -1)
target_setup = (-1, -1, -1, 0, 1, 1, 1)

print("DFS Search Result:")
dfs_solution = depth_first(initial_setup, target_setup)
if dfs_solution:
    print("Path found!")
    print("Step count:", len(dfs_solution) - 1)
    for step in dfs_solution:
        print(step)
else:
    print("No solution found.")

print("\nBFS Search Result:")
bfs_solution = breadth_first(initial_setup, target_setup)
if bfs_solution:
    print("Path found!")
    print("Step count:", len(bfs_solution) - 1)
    for step in bfs_solution:
        print(step)
else:
    print("No solution found.")