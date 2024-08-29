import pygame
import random
import numpy as np
import tensorflow as tf
from collections import deque

# Pong Game
class PongGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 60
        self.ball_size = 10
        self.paddle_speed = 5
        self.ball_speed_x = 3
        self.ball_speed_y = 3

        self.paddle1_pos = height // 2 - self.paddle_height // 2
        self.paddle2_pos = height // 2 - self.paddle_height // 2
        self.ball_pos = [width // 2, height // 2]

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()

    def reset(self):
        self.paddle1_pos = self.height // 2 - self.paddle_height // 2
        self.paddle2_pos = self.height // 2 - self.paddle_height // 2
        self.ball_pos = [self.width // 2, self.height // 2]
        self.ball_speed_x = 3 * random.choice([-1, 1])
        self.ball_speed_y = 3 * random.choice([-1, 1])
        return self.get_state()

    def step(self, action):
        reward = 0
        done = False

        # Move paddle2 (AI-controlled)
        if action == 0:  # Move up
            self.paddle2_pos = max(0, self.paddle2_pos - self.paddle_speed)
        elif action == 1:  # Move down
            self.paddle2_pos = min(self.height - self.paddle_height, self.paddle2_pos + self.paddle_speed)

        # Move paddle1 (simple AI)
        if self.ball_pos[1] > self.paddle1_pos + self.paddle_height // 2:
            self.paddle1_pos = min(self.height - self.paddle_height, self.paddle1_pos + self.paddle_speed)
        elif self.ball_pos[1] < self.paddle1_pos + self.paddle_height // 2:
            self.paddle1_pos = max(0, self.paddle1_pos - self.paddle_speed)

        # Move ball
        self.ball_pos[0] += self.ball_speed_x
        self.ball_pos[1] += self.ball_speed_y

        # Ball collision with top and bottom
        if self.ball_pos[1] <= 0 or self.ball_pos[1] >= self.height - self.ball_size:
            self.ball_speed_y *= -1

        # Ball collision with paddles
        if self.ball_pos[0] <= self.paddle_width and self.paddle1_pos <= self.ball_pos[1] <= self.paddle1_pos + self.paddle_height:
            self.ball_speed_x *= -1
            reward = -1  # Opponent scored a point
        elif self.ball_pos[0] >= self.width - self.paddle_width - self.ball_size and self.paddle2_pos <= self.ball_pos[1] <= self.paddle2_pos + self.paddle_height:
            self.ball_speed_x *= -1
            reward = 1  # Agent scored a point

        # Ball out of bounds
        if self.ball_pos[0] < 0 or self.ball_pos[0] > self.width:
            done = True
            reward = -1 if self.ball_pos[0] < 0 else 1

        return self.get_state(), reward, done

    def get_state(self):
        return [
            self.paddle1_pos / self.height,
            self.paddle2_pos / self.height,
            self.ball_pos[0] / self.width,
            self.ball_pos[1] / self.height,
            self.ball_speed_x / max(abs(self.ball_speed_x), abs(self.ball_speed_y)),
            self.ball_speed_y / max(abs(self.ball_speed_x), abs(self.ball_speed_y))
        ]

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), (0, self.paddle1_pos, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.width - self.paddle_width, self.paddle2_pos, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.ball_pos[0], self.ball_pos[1], self.ball_size, self.ball_size))
        pygame.display.flip()
        self.clock.tick(60)
    
    def close(self):
        pygame.quit()

# DQN Agent
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            tf.keras.layers.Dense(24, activation='relu'),
            tf.keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

# Training script
def train_dqn_agent():
    env = PongGame()
    state_size = 6
    action_size = 3  # Up, Down, Stay
    agent = DQNAgent(state_size, action_size)
    batch_size = 32
    episodes = 1000

    for e in range(episodes):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        total_reward = 0

        for time in range(500):  # Max 500 steps per episode
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                print(f"Episode: {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2}")
                break

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            env.render()

        if e % 10 == 0:
            agent.model.save(f'pong_dqn_model_{e}.h5')

    env.close()

if __name__ == "__main__":
    with tf.device('/GPU:0'):
        train_dqn_agent()
