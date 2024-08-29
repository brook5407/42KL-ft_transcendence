# import os
# os.environ['LD_LIBRARY_PATH'] = '/usr/local/cuda/lib64:' + os.environ.get('LD_LIBRARY_PATH', '')


from game import PongGame
from dqn_agent import DQNAgent
import numpy as np
import tensorflow as tf

def main():
    # tf.profiler.experimental.start('logdir')
    env = PongGame()
    state_size = env.get_state().shape[0]
    action_size = 3
    agent = DQNAgent(state_size, action_size)
    episodes = 1000
    batch_size = 32
    target_update_interval = 10  # Update target network every 10 episodes

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(300):
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                print(f"episode: {e}/{episodes}, score: {time}, e: {agent.epsilon:.2}")
                break
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
            env.render(e)
            env.clock.tick(env.fps)
            
        # Save the model every 50 episodes
        if e % 50 == 0:
            agent.model.save(f"model_episode_{e}.h5")
    # tf.profiler.experimental.stop()

if __name__ == "__main__":
    # tf.debugging.set_log_device_placement(True)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if not gpus:
        print("No GPU detected!")
    else:
        print(f"Detected {len(gpus)} GPU(s): {gpus}")

        # Allow memory growth
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)

        # Set device to GPU explicitly
        main()