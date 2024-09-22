import numpy as np
from jump import GameEnvironment
from agent import DQNAgent

if __name__ == '__main__':
    env = GameEnvironment()
    state_dim = env.get_state().shape[0]
    action_dim = 2  # Left, Right, Jump

    agent = DQNAgent(state_dim, action_dim)
    #agent.load("model/model_640.pth")
    agent.load("model/best_model.pth")
    state = env.reset()
    state = np.array(state, dtype=np.float32)
    done = False

    while not done:
        action = agent.act(state)
        next_state, reward, done = env.step(action)
        next_state = np.array(next_state, dtype=np.float32)
        state = next_state
        env.render(True)

    env.close()
