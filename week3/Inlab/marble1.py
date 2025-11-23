import time
import heapq

class Cell:
    def __init__(self, board, prev=None, steps=0):
        self.board = board
        self.prev = prev
        self.move = None
        self.steps = steps

    def __lt__(self, other):
        return self.steps < other.steps

target_board = [
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 2, 0, 0, 0, 2, 2],
    [2, 2, 0, 0, 0, 2, 2]
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

expanded = 0

def generate_moves(cell):
    global expanded
    nxt = []
    jump2 = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    jump1 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for i in range(7):
        for j in range(7):
            if cell.board[i][j] == 1:
                for d in range(4):
                    ni, nj = i + jump2[d][0], j + jump2[d][1]
                    mi, mj = i + jump1[d][0], j + jump1[d][1]
                    if 0 <= ni < 7 and 0 <= nj < 7 and cell.board[mi][mj] == 1 and cell.board[ni][nj] == 0:
                        new_board = [row[:] for row in cell.board]
                        new_board[i][j] = 0
                        new_board[mi][mj] = 0
                        new_board[ni][nj] = 1
                        nxt_cell = Cell(new_board, cell, steps=cell.steps + 1)
                        nxt_cell.move = [(i, j), (ni, nj)]
                        nxt.append(nxt_cell)
                        expanded += 1
    return nxt

def priority_search():
    open_list = []
    visited = set()
    start = Cell(start_board)
    heapq.heappush(open_list, start)

    while open_list:
        node = heapq.heappop(open_list)
        print("Board with cost:", node.steps)
        for row in node.board:
            print(row)
        print()

        if node.board == target_board:
            print("Finished")
            return node

        visited.add(str(node.board))

        for nxt in generate_moves(node):
            if str(nxt.board) not in visited:
                heapq.heappush(open_list, nxt)

    return None

def trace_path(last):
    seq = []
    while last.prev:
        seq.append(last.move)
        last = last.prev
    return seq[::-1]

print("Search started")
t1 = time.time()
ans = priority_search()
t2 = time.time()

if ans:
    print("Expanded nodes:", expanded)
    print("Elapsed:", t2 - t1)
    print("Goal:")
    for row in ans.board:
        print(row)
    print("\nMoves:")
    steps = trace_path(ans)
    for m in steps:
        print(m)
else:
    print("No solution")