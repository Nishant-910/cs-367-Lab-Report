import time
import heapq

class StateNode:
    def __init__(self, board, parent=None, move=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f

target_board = [
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2],
    [0,0,0,0,0,0,0],
    [0,0,0,1,0,0,0],
    [0,0,0,0,0,0,0],
    [2,2,0,0,0,2,2],
    [2,2,0,0,0,2,2]
]

start_board = [
    [2, 2, 1, 1, 1, 2, 2], 
    [2, 2, 1, 1, 1, 2, 2], 
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1], 
    [1, 1, 1, 1, 1, 1, 1], 
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]

def heuristic_count(board):
    return sum(row.count(1) for row in board)

def heuristic_distance(board):
    total = 0
    for i in range(7):
        for j in range(7):
            if board[i][j] == 1:
                total += abs(i - 3) + abs(j - 3)
    return total

def generate_successors(node, heuristic):
    children = []
    jump2 = [(-2,0),(2,0),(0,-2),(0,2)]
    jump1 = [(-1,0),(1,0),(0,-1),(0,1)]

    for i in range(7):
        for j in range(7):
            if node.board[i][j] == 1:
                for k in range(4):
                    ni, nj = i + jump2[k][0], j + jump2[k][1]
                    mi, mj = i + jump1[k][0], j + jump1[k][1]
                    if 0 <= ni < 7 and 0 <= nj < 7 and node.board[mi][mj] == 1 and node.board[ni][nj] == 0:
                        new_board = [row[:] for row in node.board]
                        new_board[i][j] = 0
                        new_board[mi][mj] = 0
                        new_board[ni][nj] = 1
                        child = StateNode(new_board, node, move=[(i,j),(ni,nj)], g=node.g+1, h=heuristic(new_board))
                        children.append(child)
    return children

def a_star(start, heuristic):
    root = StateNode(start)
    root.h = heuristic(root.board)
    open_list = []
    heapq.heappush(open_list, root)
    visited = set()

    while open_list:
        node = heapq.heappop(open_list)
        if node.board == target_board:
            print("Search completed")
            return node

        visited.add(str(node.board))
        for child in generate_successors(node, heuristic):
            if str(child.board) not in visited:
                child.h = heuristic(child.board)
                heapq.heappush(open_list, child)
    return None

def extract_path(node):
    path = []
    while node.parent:
        path.append(node.move)
        node = node.parent
    return path[::-1]

print("A* search with heuristic 1")
t1 = time.time()
result = a_star(start_board, heuristic_count)
t2 = time.time()

if result:
    print("Total cost:", result.f)
    print("Time:", t2 - t1)
    print("Moves:")
    for m in extract_path(result):
        print(m)
else:
    print("No solution found")

print("\nA* search with heuristic 2")
t1 = time.time()
result = a_star(start_board, heuristic_distance)
t2 = time.time()

if result:
    print("Total cost:", result.f)
    print("Time:", t2 - t1)
    print("Moves:")
    for m in extract_path(result):
        print(m)
else:
    print("No solution found")