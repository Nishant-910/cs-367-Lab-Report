from collections import deque
import time

def valid_config(config):
    m, c, boat_side = config
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False
    if m > 0 and c > m:
        return False
    if (3 - m) > 0 and (3 - c) > (3 - m):
        return False
    return True

def next_states(config):
    results = []
    m, c, boat_side = config
    boat_moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    if boat_side == 1:
        for mm, cc in boat_moves:
            candidate = (m - mm, c - cc, 0)
            if valid_config(candidate):
                results.append(candidate)
    else:
        for mm, cc in boat_moves:
            candidate = (m + mm, c + cc, 1)
            if valid_config(candidate):
                results.append(candidate)
    return results

def depth_first_search(start, target):
    stack = [(start, [])]
    explored = set()
    while stack:
        current, trace = stack.pop()
        if current in explored:
            continue
        explored.add(current)
        trace = trace + [current]
        if current == target:
            return trace
        for nxt in next_states(current):
            stack.append((nxt, trace))
    return None

initial = (3, 3, 1)
goal = (0, 0, 0)

dfs_start = time.time()

dfs_path = depth_first_search(initial, goal)
if dfs_path:
    print("\nDFS path discovered:")
    for step in dfs_path:
        print(step)
else:
    print("DFS could not find a solution.")

dfs_end = time.time()
print(f"DFS execution time: {dfs_end - dfs_start:.6f} seconds")