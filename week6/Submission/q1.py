import numpy as np

def rook_net(sz=8, n_it=100, thr=0, n_r=8):
    n = sz * sz
    wt = np.zeros((n, n))
    for i in range(sz):
        for j in range(sz):
            for k in range(sz):
                for l in range(sz):
                    if i == k and j != l:
                        wt[i * sz + j, k * sz + l] = -1
                    if j == l and i != k:
                        wt[i * sz + j, k * sz + l] = -1

    st = np.zeros(n, dtype=int)
    positions = np.random.choice(n, n_r, replace=False)
    for p in positions:
        st[p] = 1

    print("Initial State:")
    print(st.reshape(sz, sz))

    for _ in range(n_it):
        new_st = st.copy()
        for i in range(n):
            s = np.dot(wt[i], new_st)
            new_st[i] = 1 if s > thr else 0
        if np.array_equal(st, new_st):
            break
        st = new_st

    print("Final State:")
    print(st.reshape(sz, sz))
    return st.reshape(sz, sz)

np.random.seed(42)
sol = rook_net()
