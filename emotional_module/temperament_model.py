# import numpy as np
# import random

# class TemperamentModel:
#     def __init__(self, state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state, emotion_graph):
#         self.state_size = state_size
#         self.action_size = action_size
#         self.learning_rate = learning_rate
#         self.discount_factor = discount_factor
#         self.epsilon = epsilon
#         self.emotion_graph = emotion_graph
#         self.q_table = np.zeros(((3 ** state_size), action_size))
#         self.emotional_state = emotional_state
#     def discretize_state(self, state, num_intervals):
#         """ Дискретизирует вектор состояния.
#         Args: state: Вектор состояния (список непрерывных значений).
#         num_intervals: Количество интервалов для каждого элемента.
#         Returns: Кортеж дискретизированных значений (индексы интервалов).
#         """
#         discrete_state = []
#         for value in state:
#             interval_index = int(value * num_intervals)  # Вычисляем индекс интервала
#             if interval_index == num_intervals:  #  Обработка граничного случая (value = 1)
#                 interval_index = num_intervals - 1
#             discrete_state.append(interval_index)
#         return tuple(discrete_state)
#     def get_action(self, state):
#         # ... (код  дискретизации  state  -  без  изменений)

#         if random.uniform(0, 1) < self.epsilon:
#             return random.randrange(self.action_size)

#         discrete_state = self.discretize_state(state, num_intervals=3)
#         state_index = self.get_state_index(discrete_state, num_intervals=3) 
#         q_values = self.q_table[state_index, :] 

#         # --- Примеры влияния эмоций на выбор действия ---

#         joy_intensity = self.emotional_state.get_emotion_intensity(0)
#         q_values[0] += joy_intensity * 0.5

#         sadness_intensity = self.emotional_state.get_emotion_intensity(1)
#         q_values[1:4] -= sadness_intensity * 0.3 
#         q_values = self.q_table[state_index, :] 

#         #  ---  Примеры  влияния  эмоций  на  выбор  действия  ---

#         #  0 - Выразить  радость
#         #  1 - Проявить  грусть
#         #  2 - Проявить  гнев
#         #  3 - Избегать  опасности
#         #  4 - Взаимодействовать  с  объектом
#         #  5 - Не  выражать  эмоций

#         #  1.  Радость:  усиливаем  желание  выразить  радость  и  ослабляем  негативные  эмоции
#         joy_intensity = self.emotional_state.get_emotion_intensity(0)
#         q_values[0] += joy_intensity * 0.5  
#         q_values[2] -= joy_intensity * 0.3  #  Ослабляем  гнев
#         q_values[3] -= joy_intensity * 0.4  #  Ослабляем  страх
#         q_values[5] -= joy_intensity * 0.2  #  Ослабляем  склонность  не  выражать  эмоций

#         #  2.  Грусть:  ослабляем  желание  действовать  активно  и  усиливаем  страх
#         sadness_intensity = self.emotional_state.get_emotion_intensity(1)
#         q_values[:4] -= sadness_intensity * 0.3 
#         q_values[3] += sadness_intensity * 0.5 

#         #  3.  Гнев:  усиливаем  желание  проявить  агрессию  и  ослабляем  страх
#         anger_intensity = self.emotional_state.get_emotion_intensity(2)
#         q_values[2] += anger_intensity * 0.7  
#         q_values[3] -= anger_intensity * 0.4  

#         #  4.  Страх:  усиливаем  желание  избегать  опасности  и  ослабляем  радость
#         fear_intensity = self.emotional_state.get_emotion_intensity(3)
#         q_values[3] += fear_intensity * 0.8  
#         q_values[0] -= fear_intensity * 0.2  

#         #  5.  Удивление:  делаем  выбор  действия  более  случайным
#         surprise_intensity = self.emotional_state.get_emotion_intensity(4)
#         self.epsilon += surprise_intensity * 0.2

#         #  6.  Отвращение:  ослабляем  желание  взаимодействовать  с  объектом  и  усиливаем  гнев
#         disgust_intensity = self.emotional_state.get_emotion_intensity(5)
#         q_values[4] -= disgust_intensity * 0.6  
#         q_values[2] += disgust_intensity * 0.3

#         #  ---  Примеры  влияния  EmotionGraph  на  выбор  действия  ---

#         #  1.  Гнев  подавляет  страх
#         fear_index = self.emotional_state.emotions.index("fear")
#         anger_influence_on_fear = self.emotion_graph.get_influence("anger", "fear")
#         q_values[fear_index] -= anger_influence_on_fear * anger_intensity

#         #  2.  Радость  усиливает  удивление
#         surprise_index = self.emotional_state.emotions.index("surprise")
#         joy_influence_on_surprise = self.emotion_graph.get_influence("joy", "surprise")
#         q_values[surprise_index] += joy_influence_on_surprise * joy_intensity

#         # ... (добавьте  другие  примеры  взаимодействия  из  EmotionGraph)

#         return np.argmax(q_values)    

#     def update_q_table(self, state, action, reward, next_state):
#         # SARSA update
#         current_q = self.q_table[state, action]
#         next_action = self.get_action(next_state)
#         next_q = self.q_table[next_state, next_action]

#         new_q = current_q + self.learning_rate * (reward + self.discount_factor * next_q - current_q)
#         self.q_table[state, action] = new_q
        
#     def get_state_index(self, discrete_state, num_intervals):
#         """ Преобразует кортеж индексов в одно число (индекс состояния). """
#         return sum(value * (num_intervals ** i) for i, value in enumerate(discrete_state))

import numpy as np
import random

class TemperamentModel:
    def __init__(self, state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state, emotion_graph):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.emotion_graph = emotion_graph
        self.q_table = np.zeros(((3 ** state_size), action_size))
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
        # ... (код  дискретизации  state  -  без  изменений)

        if random.uniform(0, 1) < self.epsilon:
            return random.randrange(self.action_size)

        discrete_state = self.discretize_state(state, num_intervals=3)
        state_index = self.get_state_index(discrete_state, num_intervals=3) 
        q_values = self.q_table[state_index, :] 

        #  ---  Примеры  влияния  эмоций  на  выбор  действия  ---

        #  0 - Выразить  радость
        #  1 - Проявить  грусть
        #  2 - Проявить  гнев
        #  3 - Избегать  опасности
        #  4 - Взаимодействовать  с  объектом
        #  5 - Не  выражать  эмоций

        #  1.  Радость:  усиливаем  желание  выразить  радость  и  ослабляем  негативные  эмоции
        joy_intensity = self.emotional_state.get_emotion_intensity(0)
        q_values[0] += joy_intensity * 0.5  
        q_values[2] -= joy_intensity * 0.3
        q_values[3] -= joy_intensity * 0.4 
        q_values[5] -= joy_intensity * 0.2  

        #  2.  Грусть:  ослабляем  желание  действовать  активно  и  усиливаем  страх
        sadness_intensity = self.emotional_state.get_emotion_intensity(1)
        q_values[:4] -= sadness_intensity * 0.3 
        q_values[3] += sadness_intensity * 0.5 

        #  3.  Гнев:  усиливаем  желание  проявить  агрессию  и  ослабляем  страх
        anger_intensity = self.emotional_state.get_emotion_intensity(2)
        q_values[2] += anger_intensity * 0.7  
        q_values[3] -= anger_intensity * 0.4  

        #  4.  Страх:  усиливаем  желание  избегать  опасности  и  ослабляем  радость
        fear_intensity = self.emotional_state.get_emotion_intensity(3)
        q_values[3] += fear_intensity * 0.8  
        q_values[0] -= fear_intensity * 0.2  

        #  5.  Удивление:  делаем  выбор  действия  более  случайным
        surprise_intensity = self.emotional_state.get_emotion_intensity(4)
        self.epsilon += surprise_intensity * 0.2

        #  6.  Отвращение:  ослабляем  желание  взаимодействовать  с  объектом  и  усиливаем  гнев
        disgust_intensity = self.emotional_state.get_emotion_intensity(5)
        q_values[4] -= disgust_intensity * 0.6  
        q_values[2] += disgust_intensity * 0.3

        #  ---  Примеры  влияния  EmotionGraph  на  выбор  действия  ---

        #  1.  Гнев  подавляет  страх
        fear_index = self.emotional_state.emotions.index("fear")
        anger_influence_on_fear = self.emotion_graph.get_influence("anger", "fear")
        q_values[fear_index] -= anger_influence_on_fear * anger_intensity

        #  2.  Радость  усиливает  удивление
        surprise_index = self.emotional_state.emotions.index("surprise")
        joy_influence_on_surprise = self.emotion_graph.get_influence("joy", "surprise")
        q_values[surprise_index] += joy_influence_on_surprise * joy_intensity

        # ... (добавьте  другие  примеры  взаимодействия  из  EmotionGraph)

        return np.argmax(q_values)    

    def update_q_table(self, state, action, reward, next_state):
        # ... (код  обновления  Q-таблицы  -  без  изменений)
        
    def get_state_index(self, discrete_state, num_intervals):
        """ Преобразует кортеж индексов в одно число (индекс состояния). """
        return sum(value * (num_intervals ** i) for i, value in enumerate(discrete_state))