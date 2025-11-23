import numpy as np
import matplotlib.pyplot as plt

class bibandit:
    def __init__(self, name, probabilities):
        self.name = name
        self.probabilities = probabilities
    
    def pull(self, action):
        if action < 0 or action >= len(self.probabilities):
            raise ValueError("Invalid action")
        return np.random.random() < self.probabilities[action]

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

def simulation(env, n_steps, epsilon):
    agent = epgreedy(len(env.probabilities), epsilon)
    rewards = np.zeros(n_steps)
    optimal_arm = np.argmax(env.probabilities)
    optimal_count = 0
    
    for t in range(n_steps):
        arm = agent.select_arm()
        reward = env.pull(arm)
        agent.update(arm, reward)
        rewards[t] = reward
        if arm == optimal_arm:
            optimal_count += 1
            
    return agent, rewards, optimal_count

def plot_results(env, agent, rewards, n_steps):
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    actions = np.array(agent.action_history)
    for arm in range(len(env.probabilities)):
        freq = np.cumsum(actions == arm) / (np.arange(len(actions)) + 1)
        plt.plot(freq, label=f'Arm {arm+1} (p={env.probabilities[arm]})')
    plt.xlabel('Steps')
    plt.ylabel('Selection Probability')
    plt.title(f'{env.name}: Arm Selection Probability Over Time')
    plt.legend()

    plt.subplot(2, 2, 2)
    cum_avg = np.cumsum(rewards) / (np.arange(len(rewards)) + 1)
    plt.plot(cum_avg)
    plt.xlabel('Steps')
    plt.ylabel('Average Reward')
    plt.title(f'{env.name}: Average Reward Over Time')

    optimal_actions = sum(actions == np.argmax(env.probabilities))
    print(f"\n{env.name} Results:")
    print(f"Total Reward: {np.sum(rewards)}")
    print(f"Average Reward: {np.mean(rewards):.3f}")
    print(f"Optimal Action Percentage: {100 * optimal_actions / n_steps:.1f}%")
    print("\nArm Statistics:")
    for i, p in enumerate(env.probabilities):
        print(f"Arm {i+1}:")
        print(f"  True Probability: {p:.2f}")
        print(f"  Estimated Value: {agent.values[i]:.3f}")
        print(f"  Times Selected: {int(agent.counts[i])}")

def main():
    n_steps = 1000
    epsilon = 0.1
    
    bandit_A = bibandit("Bandit A", [0.1, 0.2])
    bandit_B = bibandit("Bandit B", [0.8, 0.9])
    
    for env in [bandit_A, bandit_B]:
        agent, rewards, _ = simulation(env, n_steps, epsilon)
        plot_results(env, agent, rewards, n_steps)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
