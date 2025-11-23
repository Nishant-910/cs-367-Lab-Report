import numpy as np
import matplotlib.pyplot as plt

class nonstatbandit:
    def __init__(self, meanreward=0):
        self.meanreward = meanreward
        self.random_walk_std = 0.01
        
    def pull(self):
        reward = np.random.normal(self.meanreward, 1.0)
        self.meanreward += np.random.normal(0, self.random_walk_std)
        return reward

class epgreedy:
    def __init__(self, n_arms, epsilon):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)
        self.action_history = []
        self.reward_history = []
    
    def select_arm(self):
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_arms)
        return np.argmax(self.values)
    
    def update(self, arm, reward):
        self.counts[arm] += 1
        n = self.counts[arm]
        v = self.values[arm]
        self.values[arm] = ((n - 1) / n) * v + (1 / n) * reward
        self.action_history.append(arm)
        self.reward_history.append(reward)

def simulation(n_steps, bandits, epsilon):
    n_arms = len(bandits)
    agent = epgreedy(n_arms, epsilon)

    rewards = np.zeros(n_steps)
    mean_hist = np.zeros((n_steps, n_arms))
    
    for t in range(n_steps):
        for i, bandit in enumerate(bandits):
            mean_hist[t, i] = bandit.meanreward
            
        arm = agent.select_arm()
        reward = bandits[arm].pull()
        agent.update(arm, reward)
        rewards[t] = reward
            
    return agent, rewards, mean_hist

n_steps = 1000
epsilon = 0.1
n_arms = 10

bandits = [nonstatbandit() for _ in range(n_arms)]
agent_ns, rewards_ns, mean_hist = simulation(n_steps, bandits, epsilon)

plt.figure(figsize=(15, 10))
plt.subplot(2, 2, 1)
window = 50
moving_avg = np.convolve(rewards_ns, np.ones(window) / window, mode='valid')
plt.plot(moving_avg)
plt.xlabel('Steps')
plt.ylabel('Average Reward')
plt.title('Average Reward Over Time')
plt.show()

print("\nNon-stationary Bandit Results:")
print(f"Total Reward: {np.sum(rewards_ns)}")
print(f"Average Reward: {np.mean(rewards_ns):.3f}")

print("\nFinal Arm Statistics:")
for i in range(n_arms):
    print(f"Arm {i+1}:")
    print(f"  Final Mean Reward: {mean_hist[-1, i]:.3f}")
    print(f"  Estimated Value: {agent_ns.values[i]:.3f}")
    print(f"  Times Selected: {int(agent_ns.counts[i])}")
