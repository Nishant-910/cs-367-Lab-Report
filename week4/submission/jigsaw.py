import random
import math

def evaluate_cost(grid):
    total_cost = 0
    for row in range(512):
        for col in range(512):
            if col + 1 != 512 and (col + 1) % 128 == 0:
                total_cost += abs(int(grid[(512*row) + col]) - int(grid[(512*row) + col + 1]))
            if row + 1 != 512 and (row + 1) % 128 == 0:
                total_cost += abs(int(grid[(512*row) + col]) - int(grid[(512*(row+1)) + col]))
    return total_cost

def exchange_blocks(grid):
    block_a, block_b = random.sample(range(16), 2)
    ra, ca = divmod(block_a, 4)
    rb, cb = divmod(block_b, 4)

    row_a, row_b = 128*ra, 128*rb
    col_a, col_b = 128*ca, 128*cb

    block_data_a = []
    block_data_b = []

    for r in range(128):
        for c in range(128):
            block_data_a.append(grid[(512*(row_a + r)) + (col_a + c)])
            block_data_b.append(grid[(512*(row_b + r)) + (col_b + c)])

    for r in range(128):
        for c in range(128):
            grid[(512*(row_a + r)) + (col_a + c)] = block_data_b[(r*128)+c]
            grid[(512*(row_b + r)) + (col_b + c)] = block_data_a[(r*128)+c]

    return grid

def anneal(grid, initial_temp, cooling_factor, final_temp):
    best_cost = float('inf')
    best_grid = []
    T = initial_temp
    current_grid = grid[:]
    current_cost = evaluate_cost(current_grid)

    while T > final_temp:
        candidate_grid = exchange_blocks(current_grid.copy())
        candidate_cost = evaluate_cost(candidate_grid)

        if candidate_cost < current_cost:
            current_grid = candidate_grid
            current_cost = candidate_cost
            if current_cost < best_cost:
                best_cost = current_cost
                best_grid = current_grid.copy()
        else:
            prob = math.exp((current_cost - candidate_cost) / T)
            if random.random() < prob:
                current_grid = candidate_grid
                current_cost = candidate_cost

        T *= cooling_factor

    return best_grid, best_cost

scrambled = []
with open('week4/submission/scrambled_lena.mat', 'r') as f:
    for _ in range(5):
        next(f)
    for line in f:
        scrambled.append(line)

final_solution = []
lowest_cost = float('inf')

for _ in range(5):
    temp_start = 1000
    alpha = 0.99
    stop_temp = 0.1
    result_grid, result_cost = anneal(scrambled, temp_start, alpha, stop_temp)

    if result_cost < lowest_cost:
        lowest_cost = result_cost
        final_solution = result_grid.copy()
        scrambled = final_solution.copy()

    print(result_cost)

with open('answer.mat', 'w') as f:
    for line in final_solution:
        f.write(f"{line}")
