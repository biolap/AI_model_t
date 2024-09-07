# from tensorflow import keras
# import numpy as np
# from .emotion_graph import EmotionGraph

# class EmotionalStabilityModel:
#     def __init__(self, input_shape, emotion_graph: EmotionGraph, emotional_state, lstm_units=32):
#         self.emotion_graph = emotion_graph
#         self.emotional_state = emotional_state
#         self.num_features = len(emotional_state.emotions) + len(emotion_graph.emotions) * (len(emotion_graph.emotions) - 1)
#         self.model = keras.models.Sequential()
#         self.model.add(keras.layers.Input(shape=input_shape))
#         self.model.add(keras.layers.LSTM(lstm_units, input_shape=input_shape))
#         self.model.add(keras.layers.Dense(1, activation='sigmoid'))
#         self.model.compile(loss='mse', optimizer='adam')

#     def predict_emotional_stability(self, input_data):
#         prediction = self.model.predict(input_data) 
#         return prediction[0][0]

#     def train(self, X_train, y_train, epochs=100, batch_size=32):
#         self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
#     def prepare_data(self, emotional_history):
#         X = []
#         y = []
#         for i in range(len(emotional_history) - 5):
#             #  Создаем  вектор  признаков  для  каждого  шага  времени
#             features = []

#             #  1.  Добавляем  вектор  эмоционального  состояния  для  каждого  из  5  предыдущих  шагов
#             for j in range(5):  
#                 features.extend(emotional_history[i+j])  

#             #  2.  Добавляем  информацию  из  EmotionGraph  для  каждого  из  5  предыдущих  шагов
#             for j in range(5): 
#                 for emotion1 in self.emotion_graph.emotions:
#                     for emotion2 in self.emotion_graph.emotions:
#                         if emotion1 != emotion2:
#                             influence = self.emotion_graph.get_influence(emotion1, emotion2)
#                             emotion1_intensity = emotional_history[i+j][self.emotional_state.emotions.index(emotion1)]
#                             features.append(influence * emotion1_intensity)

#             X.append(features)
#             y.append(emotional_history[i + 5][0])  #  Используем  радость  на  следующем  шаге  как  целевое  значение

#         #  Преобразуем  X  в  нужную  форму
#         X = np.array(X).reshape(len(X), 5, self.num_features)  #  (samples,  timesteps,  features)
#         return  X,  np.array(y)
    
    
from tensorflow import keras
import numpy as np
from .emotion_graph import EmotionGraph

class EmotionalStabilityModel:
    def __init__(self, input_shape, emotion_graph: EmotionGraph, emotional_state, lstm_units=32):
        self.emotion_graph = emotion_graph
        self.emotional_state = emotional_state
        self.input_shape = input_shape
        self.num_emotions = len(self.emotional_state.emotions)
        self.num_features = self.num_emotions + self.num_emotions * (self.num_emotions - 1)

        # Создание модели
        self.model = keras.models.Sequential()

        # 1. LSTM слой для обработки истории эмоциональных состояний
        self.model.add(keras.layers.LSTM(lstm_units, input_shape=input_shape))

        # 2. Dense слой для обработки текущего эмоционального состояния
        self.model.add(keras.layers.Input(shape=(self.num_emotions,)))  
        self.model.add(keras.layers.Dense(self.num_emotions, activation='relu'))

        # 3. Dense слой для обработки матрицы весов EmotionGraph
        self.model.add(keras.layers.Input(shape=(self.num_emotions, self.num_emotions))) 
        self.model.add(keras.layers.Flatten()) 
        self.model.add(keras.layers.Dense(self.num_emotions ** 2, activation='relu'))

        # 4. Объединяем выходы всех слоев
        self.model.add(keras.layers.Concatenate())

        # 5. Финальный Dense слой с sigmoid активацией 
        self.model.add(keras.layers.Dense(1, activation='sigmoid'))

        # Компиляция модели
        self.model.compile(loss='mse', optimizer='adam')

    def predict_emotional_stability(self, current_emotional_state, emotional_history, emotion_graph_weights):
        """ Предсказывает эмоциональную устойчивость. """
        input_data = self.prepare_input(current_emotional_state, emotional_history, emotion_graph_weights)
        prediction = self.model.predict(input_data)
        return prediction[0][0]

    def train(self, X_train, y_train, epochs=100, batch_size=32):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def prepare_data(self, emotional_history):
        X = []
        y = []
        for i in range(len(emotional_history) - 5):
            features = []

            #  1. Добавляем вектор эмоционального состояния для каждого из 5 предыдущих шагов
            for j in range(5):  
                features.extend(emotional_history[i+j])  

            #  2.  Добавляем  информацию  из  EmotionGraph  для  каждого  из  5  предыдущих  шагов
            for j in range(5): 
                for emotion1 in self.emotion_graph.emotions:
                    for emotion2 in self.emotion_graph.emotions:
                        if emotion1 != emotion2:
                            influence = self.emotion_graph.get_influence(emotion1, emotion2)
                            emotion1_intensity = emotional_history[i+j][self.emotional_state.emotions.index(emotion1)]
                            features.append(influence * emotion1_intensity)

            X.append(features)
            y.append(emotional_history[i + 5][0])  # Используем радость на следующем шаге как целевое значение

        #  Преобразуем  X  в  нужную  форму
        X = np.array(X).reshape(len(X), 5, self.num_features)  #  (samples,  timesteps,  features)
        return X, np.array(y)
        
    def prepare_input(self, current_emotional_state, emotional_history, emotion_graph_weights):
        """ Подготавливает входные данные для модели. """
        # Преобразование истории эмоций в нужную форму для LSTM
        emotional_history = np.array(emotional_history).reshape(1, self.input_shape[0], self.num_emotions)  
        # Создание списка входных данных для модели
        return [emotional_history, current_emotional_state, emotion_graph_weights]
    
    def generate_training_data(self, num_samples):
        """ Генерирует искусственный набор данных для обучения.

        Args:
            num_samples: Количество примеров в наборе данных.

        Returns:
            X_train: Массив входных данных.
            y_train: Массив выходных данных (эмоциональная устойчивость).
        """
        X_train = []
        y_train = []

        for _ in range(num_samples):
            # 1. Генерируем случайное текущее эмоциональное состояние
            current_emotional_state = np.random.rand(self.num_emotions)

            # 2. Генерируем случайную историю эмоциональных состояний
            emotional_history = [np.random.rand(self.num_emotions) for _ in range(self.input_shape[0])]

            # 3. Используем матрицу весов из EmotionGraph
            emotion_graph_weights = self.emotion_graph.weights

            # 4. Генерируем случайное значение эмоциональной устойчивости (между 0 и 1)
            emotional_stability = np.random.rand()

            # Добавляем данные в обучающий набор
            X_train.append([current_emotional_state, emotional_history, emotion_graph_weights])
            y_train.append(emotional_stability)

        return np.array(X_train), np.array(y_train)