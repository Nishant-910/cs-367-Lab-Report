import numpy as np

def iterate_values(cost_step=0.02, disc=0.9, tol=1e-4):
    h, w = 3, 4
    grid = np.zeros((h, w))

    grid[0, 3] = 1
    grid[1, 3] = -1

    moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while True:
        diff = 0
        prev = grid.copy()

        for i in range(h):
            for j in range(w):

                if (i, j) in [(0, 3), (1, 3), (1, 1)]:
                    continue

                vals = []

                for mv in moves:
                    tmp = 0

                    nr, nc = i + mv[0], j + mv[1]

                    if 0 <= nr < h and 0 <= nc < w and (nr, nc) != (1, 1):
                        tmp += 0.8 * (cost_step + disc * prev[nr, nc])
                    else:
                        tmp += 0.8 * (cost_step + disc * prev[i, j])

                    left_m = (mv[1], -mv[0])
                    lr, lc = i + left_m[0], j + left_m[1]

                    if 0 <= lr < h and 0 <= lc < w and (lr, lc) != (1, 1):
                        tmp += 0.1 * (cost_step + disc * prev[lr, lc])
                    else:
                        tmp += 0.1 * (cost_step + disc * prev[i, j])

                    right_m = (-mv[1], mv[0])
                    rr, rc = i + right_m[0], j + right_m[1]

                    if 0 <= rr < h and 0 <= rc < w and (rr, rc) != (1, 1):
                        tmp += 0.1 * (cost_step + disc * prev[rr, rc])
                    else:
                        tmp += 0.1 * (cost_step + disc * prev[i, j])

                    vals.append(tmp)

                grid[i, j] = max(vals)
                diff = max(diff, abs(grid[i, j] - prev[i, j]))

        if diff < tol:
            break

    return grid


ans = iterate_values()
print("Value Function for r(s) = -2:")
print(ans)
