import numpy as np
import matplotlib.pyplot as plt

class DriftArm:
    def __init__(self, mu=0):
        self.mu = mu
        self.drift = 0.01
        
    def trigger(self):
        r = np.random.normal(self.mu, 1.0)
        self.mu += np.random.normal(0, self.drift)
        return r

class GreedyEps:
    def __init__(self, k, eps, lr=0.1):
        self.k = k
        self.eps = eps
        self.ct = np.zeros(k)
        self.est = np.zeros(k)
        self.lr = lr
        self.a_log = []
        self.r_log = []
    
    def choose(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.k)
        return np.argmax(self.est)
    
    def revise(self, arm, r):
        self.ct[arm] += 1
        self.est[arm] += self.lr * (r - self.est[arm])
        self.a_log.append(arm)
        self.r_log.append(r)

def run_sim(T, arms, eps):
    k = len(arms)
    agent = GreedyEps(k, eps)
    rw = np.zeros(T)
    track_mu = np.zeros((T, k))
    
    for t in range(T):
        for idx, a in enumerate(arms):
            track_mu[t, idx] = a.mu

        pick = agent.choose()
        r = arms[pick].trigger()
        agent.revise(pick, r)
        rw[t] = r
    
    return agent, rw, track_mu


T = 10000
eps = 0.1
K = 10

env = [DriftArm() for _ in range(K)]
agent_out, rew_stream, mu_hist = run_sim(T, env, eps)

plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
w = 50
smooth = np.convolve(rew_stream, np.ones(w)/w, mode='valid')
plt.plot(smooth)
plt.xlabel('Steps')
plt.ylabel('Average Reward')
plt.title('Average Reward Over Time')
plt.show()

print("\nNon-stationary Bandit Results:")
print(f"Total Reward: {np.sum(rew_stream)}")
print(f"Average Reward: {np.mean(rew_stream):.3f}")
print("\nFinal Arm Statistics:")

for idx in range(K):
    print(f"Arm {idx+1}:")
    print(f"  Final Mean Reward: {mu_hist[-1, idx]:.3f}")
    print(f"  Estimated Value: {agent_out.est[idx]:.3f}")
    print(f"  Times Selected: {int(agent_out.ct[idx])}")
