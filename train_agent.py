import time
from motocross_env import MotocrossEnv
from q_agent import QAgent


def main():
    env = MotocrossEnv()
    agent = QAgent()
    episodes = 500
    for ep in range(episodes):
        state = env.reset()
        done = False
        ep_reward = 0.0
        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state, done)
            state = next_state
            ep_reward += reward
        if ep % 100 == 0:
            print(f"Episode {ep} reward {ep_reward:.2f}")
    # demonstrate
    state = env.reset()
    done = False
    while not done:
        action = agent.choose_action(state)
        state, reward, done = env.step(action)
        env.render()
        time.sleep(0.02)


if __name__ == "__main__":
    main()
