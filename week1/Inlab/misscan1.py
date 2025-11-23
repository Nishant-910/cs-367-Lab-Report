from collections import deque
import time

start_timer = time.time()

def check_state(config):
    m, c, boat_side = config
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False
    if m > 0 and c > m:
        return False
    if (3 - m) > 0 and (3 - c) > (3 - m):
        return False
    return True

def possible_moves(config):
    options = []
    m, c, boat_side = config
    boat_moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]
    if boat_side == 1:
        for mm, cc in boat_moves:
            nxt = (m - mm, c - cc, 0)
            if check_state(nxt):
                options.append(nxt)
    else:
        for mm, cc in boat_moves:
            nxt = (m + mm, c + cc, 1)
            if check_state(nxt):
                options.append(nxt)
    return options

def breadth_first_search(initial, target):
    q = deque([(initial, [])])
    explored = set()
    while q:
        state, route = q.popleft()
        if state in explored:
            continue
        explored.add(state)
        route = route + [state]
        if state == target:
            return route
        for nxt in possible_moves(state):
            q.append((nxt, route))
    return None

initial_state = (3, 3, 1)
target_state = (0, 0, 0)

path = breadth_first_search(initial_state, target_state)
if path:
    print("Solution path:")
    for step in path:
        print(step)
else:
    print("No valid solution.")

end_timer = time.time()
print(f"Execution time: {end_timer - start_timer:.5f} seconds")