# train.py
import numpy as np
import matplotlib.pyplot as plt
from jump import GameEnvironment
from agent import DQNAgent
from gameComponent import coinIdSet

if __name__ == '__main__':
    env = GameEnvironment()
    state_dim = env.get_state().shape[0]
    action_dim = 2  # Left(it is disabled for smoother movement), Right, Jump

    agent = DQNAgent(state_dim, action_dim)

    episodes = 1000
    rewards = []
    avg_rewards = []
    best_avg_reward = -np.inf

    # Initialize live plot
    plt.ion()
    fig, ax = plt.subplots()
    line, = ax.plot(rewards, label='Total Reward')
    avg_line, = ax.plot(avg_rewards, label=f'Average Reward (Last 100 Episodes)')
    ax.set_xlabel('Episodes')
    ax.set_ylabel('Reward')
    ax.legend()
    plt.title('Training Progress')
    plt.show()

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

        rewards.append(total_reward)
        avg_reward = np.mean(rewards[-100:])
        avg_rewards.append(avg_reward)

        # Update live plot
        line.set_xdata(range(len(rewards)))
        line.set_ydata(rewards)
        avg_line.set_xdata(range(len(avg_rewards)))
        avg_line.set_ydata(avg_rewards)
        ax.relim()
        ax.autoscale_view()
        plt.draw()
        plt.pause(0.01)  # Pause to update the plot

        agent.replay()

        # Save the model every 10 episodes
        if e % 10 == 0:
            agent.save(f"model/model_{e}.pth")

        # Save the best model
        if avg_reward > best_avg_reward:
            best_avg_reward = avg_reward
            agent.save("model/best_model.pth")

    plt.ioff()
    plt.show()
    env.close()
