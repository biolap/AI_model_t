import numpy as np
import random

class TemperamentModel:
    def  __init__(self,  state_size,  action_size,  learning_rate,  discount_factor,  epsilon,  emotional_state,  emotion_graph,  num_intervals=5):  #  Добавлен  num_intervals
        # ... (другие  атрибуты)
        self.num_intervals = num_intervals  #  Сохраняем  num_intervals  как  атрибут
        #  Размер  Q-таблицы  теперь  зависит  от  num_intervals
        # self.q_table = np.zeros(((self.num_intervals ** self.state_size), self.action_size))  # Correct size
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.emotion_graph = emotion_graph
        self.emotional_state = emotional_state
        #  Изменение:  размер  Q-таблицы  зависит  от  количества  возможных  дискретных  состояний
        self.q_table = np.zeros(((self.num_intervals ** self.state_size), self.action_size))  # Correct size
    
    def discretize_state(self, state, num_intervals):
        """  Дискретизирует  вектор  состояния  по  равномерной  сетке.  """
        discrete_state = []
        for value in state:
            interval_index = int(value * num_intervals)  #  Вычисляем  индекс  интервала
            if interval_index == num_intervals:  #  Обработка  граничного  случая  (value  =  1)
                interval_index = num_intervals - 1
            discrete_state.append(interval_index)
        return  tuple(discrete_state)

    def  get_action(self,  state):
        """  Выбирает  действие  на  основе  Q-таблицы  и  epsilon-жадности.  """
        if  random.uniform(0,  1)  <  self.epsilon:
            #  Исследование:  выбираем  случайное  действие
            return  random.randrange(self.action_size)
        else:
            #  Эксплуатация:  выбираем  действие  с  максимальной  оценкой
            discrete_state = self.discretize_state(state,  self.num_intervals)  #  Добавлен  self.num_intervals
            state_index = self.get_state_index(discrete_state,  self.num_intervals)  #  Добавлен  self.num_intervals
            return  np.argmax(self.q_table[state_index,  :])

    def update_q_table(self, state, action, reward, next_state):
        """  Обновляет  Q-таблицу  по  алгоритму  SARSA.  """
        discrete_state = self.discretize_state(state,  self.num_intervals)  #  Добавлен  self.num_intervals
        discrete_next_state = self.discretize_state(next_state, self.num_intervals)  #  Добавлен  self.num_intervals
        state_index = self.get_state_index(discrete_state, self.num_intervals)  #  Добавлен  self.num_intervals
        next_state_index = self.get_state_index(discrete_next_state, self.num_intervals)  #  Добавлен  self.num_intervals
        next_action = self.get_action(next_state)

        #  SARSA  update
        current_q = self.q_table[state_index, action]
        next_q = self.q_table[next_state_index, next_action]
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_q - current_q)
        self.q_table[state_index, action] = new_q

    def get_state_index(self, discrete_state, num_intervals):
        """  Преобразует  дискретное  состояние  в  индекс  в  Q-таблице.  """
        return sum(value * (num_intervals ** i) for i, value in enumerate(discrete_state))