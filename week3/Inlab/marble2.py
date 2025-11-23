import time

class Cell:
    def __init__(self, layout, prev=None, depth=0):
        self.layout = layout
        self.prev = prev
        self.move = None
        self.depth = depth

    def __lt__(self, other):
        return self.depth < other.depth

target_layout = [
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2]
]

start_layout = [
    [2, 2, 1, 1, 1, 2, 2], 
    [2, 2, 1, 1, 1, 2, 2], 
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1], 
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]

expanded = 0

def expand(node):
    global expanded
    next_states = []
    jump2 = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    jump1 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(7):
        for j in range(7):
            if node.layout[i][j] == 1:
                for k in range(4):
                    ni, nj = i + jump2[k][0], j + jump2[k][1]
                    mi, mj = i + jump1[k][0], j + jump1[k][1]
                    if 0 <= ni < 7 and 0 <= nj < 7 and node.layout[mi][mj] == 1 and node.layout[ni][nj] == 0:
                        new_layout = [row[:] for row in node.layout]
                        new_layout[i][j] = 0
                        new_layout[mi][mj] = 0
                        new_layout[ni][nj] = 1
                        new_node = Cell(new_layout, node, depth=node.depth + 1)
                        new_node.move = [(i, j), (ni, nj)]
                        next_states.append(new_node)
                        expanded += 1
    return next_states

def greedy_search():
    stack = []
    seen = set()
    root = Cell(start_layout)
    stack.append(root)

    while stack:
        node = stack.pop()
        print("Board with cost:", node.depth)
        for row in node.layout:
            print(row)
        print()

        if node.layout == target_layout:
            print("Goal reached")
            return node

        seen.add(str(node.layout))

        for nxt in expand(node):
            if str(nxt.layout) not in seen:
                stack.append(nxt)

    return None

def trace(goal):
    path = []
    while goal.prev:
        path.append(goal.move)
        goal = goal.prev
    return path[::-1]

print("Greedy-like Search started")
t1 = time.time()
result = greedy_search()
t2 = time.time()

if result:
    print("Expanded nodes:", expanded)
    print("Time:", t2 - t1)
    print("Final layout:")
    for row in result.layout:
        print(row)
    print("\nSequence of moves:")
    path = trace(result)
    for step in path:
        print(step)
else:
    print("No solution found")
