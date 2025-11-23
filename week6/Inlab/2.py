import numpy as np
import matplotlib.pyplot as plt

def binary_to_bipolar(p):
    return np.where(p == 0, -1, 1)

def bipolar_to_binary(p):
    return np.where(p == -1, 0, 1)

def train_hopfield(patterns):
    n = patterns[0].size
    w = np.zeros((n, n))
    for p in patterns:
        p = p.reshape(-1, 1)
        w += np.dot(p, p.T)
    np.fill_diagonal(w, 0)
    return w / len(patterns)

def recall(weights, pattern, max_iter=100):
    n = pattern.size
    s = pattern.copy()
    for _ in range(max_iter):
        for i in range(n):
            net = np.dot(weights[i], s)
            s[i] = 1 if net >= 0 else -1
    return s

def test_capacity():
    n = 100
    max_p = 30
    sz = (10, 10)
    rates = []

    for count in range(1, max_p + 1):
        patterns = [binary_to_bipolar(np.random.randint(0, 2, sz).flatten()) for _ in range(count)]
        w = train_hopfield(patterns)
        hits = 0

        for p in patterns:
            x = p.copy()
            flips = int(0.1 * n)
            idx = np.random.choice(n, flips, replace=False)
            x[idx] *= -1
            r = recall(w, x)
            if np.array_equal(r, p):
                hits += 1

        rates.append(hits / count)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_p + 1), rates, marker='o')
    plt.axvline(x=int(0.15 * n), linestyle='--', color='red', label='Theoretical Capacity (15)')
    plt.title('Hopfield Network Capacity Test')
    plt.xlabel('Number of Stored Patterns')
    plt.ylabel('Recall Success Rate')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    test_capacity()
