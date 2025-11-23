import numpy as np

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

def recall(w, x, max_iter=100):
    n = x.size
    s = x.copy()
    for _ in range(max_iter):
        for i in range(n):
            v = np.dot(w[i], s)
            s[i] = 1 if v >= 0 else -1
    return s

if __name__ == "__main__":
    patterns = [
        np.random.randint(0, 2, (10, 10)),
        np.random.randint(0, 2, (10, 10)),
        np.random.randint(0, 2, (10, 10))
    ]

    bipolar_patterns = [binary_to_bipolar(p.flatten()) for p in patterns]
    w = train_hopfield(bipolar_patterns)

    test_pattern = patterns[0].copy()
    test_pattern[0][0] = 1 - test_pattern[0][0]
    x = binary_to_bipolar(test_pattern.flatten())

    r = recall(w, x)
    r = r.reshape(10, 10)
    r_bin = bipolar_to_binary(r)

    print("Original Pattern:")
    print(patterns[0])
    print("\nNoisy Input Pattern:")
    print(test_pattern)
    print("\nRecalled Pattern:")
    print(r_bin)
