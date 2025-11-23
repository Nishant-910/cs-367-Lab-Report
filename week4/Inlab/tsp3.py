import math
import random
import time
import os

def calc_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def path_length(path):
    return sum(calc_distance(path[i], path[(i+1) % len(path)]) for i in range(len(path)))

def simulated_annealing_tsp(coords, temp=10000, cooling=0.995, stop_temp=1e-8, max_iter=1000000):
    current_path = coords[:]
    best_path = coords[:]
    n = len(coords)
    iteration = 1

    while temp > stop_temp and iteration < max_iter:
        i, j = sorted(random.sample(range(n), 2))
        new_path = current_path[:]
        new_path[i:j+1] = reversed(new_path[i:j+1])
        curr_dist = path_length(current_path)
        new_dist = path_length(new_path)

        if new_dist < curr_dist:
            current_path = new_path
            if new_dist < path_length(best_path):
                best_path = new_path
        elif random.random() < math.exp((curr_dist - new_dist) / temp):
            current_path = new_path

        temp *= cooling
        iteration += 1

    return best_path, path_length(best_path)

def read_tsp_file(file_path):
    coords = []
    with open(file_path, 'r') as f:
        reading = False
        for line in f:
            if "NODE_COORD_SECTION" in line:
                reading = True
                continue
            if reading:
                if line.strip() == "EOF":
                    break
                parts = line.strip().split()
                if len(parts) == 3 and parts[0].isdigit():
                    coords.append((float(parts[1]), float(parts[2])))
    if not coords:
        print(f"No coordinates found in {file_path}.")
    return coords

def solve_tsp_instance(name, coords):
    start = time.time()
    _, best_dist = simulated_annealing_tsp(coords)
    end = time.time()

    print(f"Problem: {name}")
    print(f"Number of cities: {len(coords)}")
    print(f"Best distance found: {best_dist:.2f}")
    print(f"Time taken: {end - start:.2f} seconds")
    print("--------------------")

    return best_dist, end - start

tsp_paths = [
    "C:/Users/5510/Desktop/Lab solutions/week4/Inlab/xqf131.tsp",
    "C:/Users/5510/Desktop/Lab solutions/week4/Inlab/xqg237.tsp",
    "C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pbk411.tsp",
    "C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pbn423.tsp",
    "C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pka379.tsp",
    "C:/Users/5510/Desktop/Lab solutions/week4/Inlab/pma343.tsp",
]

results = {}

for path in tsp_paths:
    if os.path.exists(path):
        coords = read_tsp_file(path)
        if coords:
            name = os.path.splitext(path)[0]
            results[name] = solve_tsp_instance(name, coords)
    else:
        print(f"File not found: {path}")

print("\nSummary of results:")
for name, (dist, duration) in results.items():
    print(f"{name}: Distance = {dist:.2f}, Time = {duration:.2f}s")