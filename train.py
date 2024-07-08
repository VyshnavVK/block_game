# train.py
import numpy as np
from jump import GameEnvironment
from agent import DQNAgent
from gameComponent import coinIdSet

if __name__ == '__main__':
    env = GameEnvironment()
    state_dim = env.get_state().shape[0]
    action_dim = 2  # Left(it is disabled for smoother movement), Right, Jump

    agent = DQNAgent(state_dim, action_dim)

    episodes = 1000
    for e in range(episodes):
        state = env.reset()
        state = np.array(state, np.float32)
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = np.array(next_state, np.float32)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward
            env.render()
            if len(coinIdSet) >= 3:
                env.reset()
            if 2 in coinIdSet and not 1:
                env.reset()

            if done:
                agent.update_target_model()
                print(f"Episode {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2}")

        agent.replay()

        if e % 10 == 0:
            agent.save(f"model/model_{e}.pth")

    env.close()
