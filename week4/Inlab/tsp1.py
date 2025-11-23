import math
import random
import time

def calc_distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)

def tour_length(path):
    return sum(calc_distance(path[i], path[(i+1) % len(path)]) for i in range(len(path)))

def generate_cities(count, max_coord):
    return [(random.randint(0, max_coord), random.randint(0, max_coord)) for _ in range(count)]

def nearest_neighbor_heuristic(city_list):
    remaining = city_list[1:]
    path = [city_list[0]]
    while remaining:
        nearest = min(remaining, key=lambda c: calc_distance(path[-1], c))
        path.append(nearest)
        remaining.remove(nearest)
    return path

def two_opt(path):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue
                new_path = path[:i] + path[i:j][::-1] + path[j:]
                if tour_length(new_path) < tour_length(path):
                    path = new_path
                    improved = True
    return path

def solve_tsp(city_list):
    start = time.time()
    initial_path = nearest_neighbor_heuristic(city_list)
    optimized_path = two_opt(initial_path)
    end = time.time()
    return optimized_path, tour_length(optimized_path), end - start

num_cities = 20
max_coord = 100

cities = generate_cities(num_cities, max_coord)

best_path, best_dist, exec_time = solve_tsp(cities)

print(f"Number of cities: {num_cities}")
print(f"Best tour distance: {best_dist:.2f}")
print(f"Execution time: {exec_time:.4f} seconds")
print("Best tour:")
for c in best_path:
    print(f"({c[0]}, {c[1]})")