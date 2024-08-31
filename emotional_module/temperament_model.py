import numpy as np
import random

class TemperamentModel:
    def __init__(self, state_size, action_size, learning_rate, discount_factor, epsilon):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((state_size, action_size))

    # ... (остальной код будет добавлен позже)
    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            # Выбираем случайное действие
            return random.randrange(self.action_size)
        else:
            # Выбираем действие с максимальной оценкой в Q-таблице
            return np.argmax(self.q_table[state, :])
    def update_q_table(self, state, action, reward, next_state):
        # SARSA update
        current_q = self.q_table[state, action]
        next_action = self.get_action(next_state)
        next_q = self.q_table[next_state, next_action]

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_q - current_q)
        self.q_table[state, action] = new_q