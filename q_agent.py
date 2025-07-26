import numpy as np
import random

class QAgent:
    """Tabular Q-learning agent for the motocross environment."""

    def __init__(self, pos_bins=20, vel_bins=20, actions=(-1, 0, 1), alpha=0.1, gamma=0.99, epsilon=0.1):
        self.pos_bins = pos_bins
        self.vel_bins = vel_bins
        self.actions = list(actions)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q = np.zeros((pos_bins, vel_bins, len(self.actions)), dtype=np.float32)

    def discretize(self, state):
        pos, vel, _ = state
        pos_bin = int(min(self.pos_bins - 1, max(0, pos / 100 * self.pos_bins)))
        vel = max(-3.0, min(3.0, vel))
        vel_bin = int((vel + 3.0) / 6.0 * (self.vel_bins - 1))
        return pos_bin, vel_bin

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        pos_bin, vel_bin = self.discretize(state)
        idx = int(np.argmax(self.q[pos_bin, vel_bin]))
        return self.actions[idx]

    def update(self, state, action, reward, next_state, done):
        pos_bin, vel_bin = self.discretize(state)
        next_pos_bin, next_vel_bin = self.discretize(next_state)
        a_idx = self.actions.index(action)
        target = reward
        if not done:
            target += self.gamma * float(np.max(self.q[next_pos_bin, next_vel_bin]))
        current = self.q[pos_bin, vel_bin, a_idx]
        self.q[pos_bin, vel_bin, a_idx] = (1 - self.alpha) * current + self.alpha * target
