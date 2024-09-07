from tensorflow import keras
import numpy as np
from .emotion_graph import EmotionGraph

class  EmotionalStabilityModel:
    def  __init__(self,  input_shape,  emotion_graph:  EmotionGraph,  emotional_state,  lstm_units=32):
        self.emotion_graph = emotion_graph
        self.emotional_state = emotional_state
        self.input_shape = input_shape
        self.num_emotions = len(self.emotional_state.emotions)
        self.num_features = self.num_emotions + self.num_emotions * (self.num_emotions - 1)

        #  1.  Входной  слой  для  истории  эмоциональных  состояний
        input_history = keras.layers.Input(shape=(input_shape[0],  self.num_emotions))
        lstm_out = keras.layers.LSTM(lstm_units,  return_sequences=True)(input_history)  #  Первый  LSTM  слой
        lstm_out = keras.layers.LSTM(lstm_units)(lstm_out)  #  Второй  LSTM  слой

        #  2.  Входной  слой  для  текущего  эмоционального  состояния
        input_current_state = keras.layers.Input(shape=(self.num_emotions,))
        dense_current_state = keras.layers.Dense(self.num_emotions,  activation='relu')(input_current_state)

        #  3.  Входной  слой  для  матрицы  весов  EmotionGraph
        input_graph_weights = keras.layers.Input(shape=(self.num_emotions,  self.num_emotions))
        flatten_graph_weights = keras.layers.Flatten()(input_graph_weights)
        dense_graph_weights = keras.layers.Dense(self.num_emotions  **  2,  activation='relu')(flatten_graph_weights)

        #  4.  Объединяем  выходы  LSTM,  Dense  для  current_state  и  Dense  для  graph_weights
        merged = keras.layers.Concatenate()([lstm_out,  dense_current_state,  dense_graph_weights])

        #  5.  Финальный  Dense  слой  с  sigmoid  активацией
        output = keras.layers.Dense(1,  activation='sigmoid')(merged)

        #  Создаем  модель  с  тремя  входами  и  одним  выходом
        self.model = keras.models.Model(inputs=[input_history,  input_current_state,  input_graph_weights],  outputs=output)

        #  Компиляция  модели
        self.model.compile(loss='mse',  optimizer='adam')
    def predict_emotional_stability(self, current_emotional_state, emotional_history, emotion_graph_weights):
        """ Предсказывает эмоциональную устойчивость. """
        #  Преобразование  истории  эмоций  в  нужную  форму
        emotional_history = np.array(emotional_history).reshape(1,  self.input_shape[0],  self.num_emotions)  
        
        #  Преобразование  в  двухмерные  массивы  с  одной  строкой
        current_emotional_state = np.array(current_emotional_state).reshape(1,  -1)
        emotion_graph_weights = np.array(emotion_graph_weights).reshape(1, self.num_emotions, self.num_emotions)

        # Передаем три аргумента в model.predict
        prediction = self.model.predict([emotional_history, current_emotional_state, emotion_graph_weights])
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
        """  Подготавливает  входные  данные  для  модели.  """
        #  Преобразование  истории  эмоций  в  нужную  форму  для  LSTM
        emotional_history = np.array(emotional_history).reshape(1, self.input_shape[0], self.num_emotions)

        #  Преобразование  в  двухмерные  массивы  с  одной  строкой
        current_emotional_state = np.array(current_emotional_state).reshape(1,  -1)
        emotion_graph_weights_flat = np.array(emotion_graph_weights).flatten().reshape(1,  -1)

        #  Создание  тензора  входных  данных
        #  Изменено:  берем  первую  строку  из  emotional_history
        input_data = np.concatenate((emotional_history[:,  0,  :],  current_emotional_state,  emotion_graph_weights_flat),  axis=1)  
        input_data = input_data.reshape(1,  self.input_shape[0],  self.num_features  +  self.num_emotions  +  self.num_emotions  *  self.num_emotions)
        return  input_data
    
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
            
            #  Печать  размерностей  перед  преобразованием  в  NumPy  массивы
            # print("Shape  of  current_emotional_state:",  np.array(current_emotional_state).shape)
            # print("Shape  of  emotional_history:",  np.array(emotional_history).shape)
            # print("Shape  of  emotion_graph_weights:",  np.array(emotion_graph_weights).shape)
            
            #  Преобразование  в  векторы  фиксированной  длины
            current_emotional_state_flat = np.array(current_emotional_state).flatten()  #  (6,)
            emotional_history_flat = np.array(emotional_history).flatten()  #  (30,)
            emotion_graph_weights_flat = np.array(emotion_graph_weights).flatten()  #  (36,)

            #  Объединение  векторов  в  один  вектор  признаков
            features = np.concatenate((
                current_emotional_state_flat, 
                emotional_history_flat, 
                emotion_graph_weights_flat
            ))  #  (72,)

            #  Добавляем  вектор  признаков  в  X_train
            X_train.append(features)
            y_train.append(emotional_stability)

        return np.array(X_train), np.array(y_train)