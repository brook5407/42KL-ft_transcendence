# dqn_agent.py
import numpy as np
import tensorflow as tf
from collections import deque
import random

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size  # Size of the state space
        self.action_size = action_size  # Size of the action space
        self.memory = deque(maxlen=2000)  # Experience replay memory
        self.gamma = 0.95  # Discount factor for future rewards
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.epsilon_decay = 0.995  # Decay rate for exploration probability
        self.learning_rate = 0.001  # Learning rate for the optimizer
        self.model = self._build_model()  # Build the Q-network
        self.frame_counter = 0
        self.last_action = 0

    def _build_model(self):
        with tf.device('/GPU:0'):
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, input_dim=self.state_size, activation='relu'),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dense(self.action_size, activation='linear')
            ])
            model.compile(loss='mse', optimizer=tf.keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        # Store experience in replay memory
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        with tf.device('/device:GPU:0'):
            self.frame_counter += 1
            if self.frame_counter % 4 == 0:
                return self.last_action
            # Epsilon-greedy action selection
            if np.random.rand() <= self.epsilon:
                self.last_action = random.randrange(self.action_size)  # Exploration: random action
                return self.last_action
            act_values = self.model(state, training=False)  # Exploitation: choose best action
            self.last_action = tf.argmax(act_values[0])
            return self.last_action  # Return the action with the highest Q-value

    def replay(self, batch_size):
        # Sample a minibatch of experiences from replay memory
        minibatch = random.sample(self.memory, batch_size)
        states = np.vstack([x[0] for x in minibatch])
        next_states = np.vstack([x[3] for x in minibatch])
        
        # Predict Q-values for current states and next states
        with tf.device('/device:GPU:0'):
            q_values = self.model.predict(states, batch_size=batch_size)
            q_next_values = self.model.predict(next_states, batch_size=batch_size)
        
        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = reward
            if not done:
                # Calculate the target Q-value using the Bellman equation
                target = reward + self.gamma * np.amax(q_next_values[i])
            q_values[i][action] = target  # Update the Q-value for the action taken
        
        # Train the model to fit the target Q-values
        self.model.fit(states, q_values, epochs=1, verbose=0, batch_size=batch_size)
        
        # Decay the exploration rate
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        
        if len(self.memory) > 100:
            self.memory.popleft()

    def load(self, name):
        # Load model weights from a file
        self.model.load_weights(name)

    def save(self, name):
        # Save model weights to a file
        self.model.save_weights(name)