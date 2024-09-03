import numpy as np
import random

class TemperamentModel:
    def __init__(self, state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((state_size, action_size))
        self.emotional_state = emotional_state
    def discretize_state(self, state, num_intervals):
        """ Дискретизирует вектор состояния.
        Args: state: Вектор состояния (список непрерывных значений).
        num_intervals: Количество интервалов для каждого элемента.
        Returns: Кортеж дискретизированных значений (индексы интервалов).
        """
        discrete_state = []
        for value in state:
            interval_index = int(value * num_intervals)  # Вычисляем индекс интервала
            if interval_index == num_intervals:  #  Обработка граничного случая (value = 1)
                interval_index = num_intervals - 1
            discrete_state.append(interval_index)
        return tuple(discrete_state)
    def get_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.randrange(self.action_size)
        # Дискретизируем state
        discrete_state = self.discretize_state(state, num_intervals=3)  
        return np.argmax(self.q_table[discrete_state, :])
    def update_q_table(self, state, action, reward, next_state):
        # SARSA update
        current_q = self.q_table[state, action]
        next_action = self.get_action(next_state)
        next_q = self.q_table[next_state, next_action]

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_q - current_q)
        self.q_table[state, action] = new_q