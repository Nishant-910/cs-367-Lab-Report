import math
import random
import time

def calc_distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def total_distance(path):
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
        curr_dist = total_distance(current_path)
        new_dist = total_distance(new_path)

        if new_dist < curr_dist:
            current_path = new_path
            if new_dist < total_distance(best_path):
                best_path = new_path
        elif random.random() < math.exp((curr_dist - new_dist) / temp):
            current_path = new_path

        temp *= cooling
        iteration += 1

    return best_path, total_distance(best_path)

cities_data = [
    ("Jaipur",(26.9124, 75.7873)),
    ("Udaipur", (24.5854, 73.6684)),
    ("Jodhpur", (26.2389, 73.122)),
    ("Ajmer", (26.4499, 74.6399)),
    ("Bikaner", (28.0229, 73.3120)),
    ("Pushkar", (26.4851, 74.6100)),
    ("Chittorgarh", (24.8796, 74.6293)),
    ("Jaisalmer", (26.9157, 70.9160)),
    ("Mount Abu", (24.5921, 72.7014)),
    ("Sikar", (27.6106, 75.1393)),
    ("Neemrana", (27.9852, 76.4577)),
    ("Kota", (25.1638, 75.8644)),
    ("Tonk", (26.0899, 75.7889)),
    ("Barmer", (25.7410, 71.4280)),
    ("Bundi", (25.4472, 75.6306)),
    ("Bikaner", (26.1865, 75.0499)),
    ("Sawai Madhopur",(26.0252, 76.3397)),
    ("Fatehpur Sikri", (27.0977, 77.6616)),
    ("Bhilwara", (26.5290, 74.6100)),
    ("Mandawa", (27.1500, 75.2520)),
    ("Jhalawar", (23.5867, 76.1632))
]

coords_list = [c[1] for c in cities_data]

start = time.time()
best_path, best_dist = simulated_annealing_tsp(coords_list)
end = time.time()

print(f"Number of cities: {len(coords_list)}")
print(f"Best distance found: {best_dist:.2f}")
print(f"Time taken: {end - start:.2f} seconds")
