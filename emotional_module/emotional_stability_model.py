from tensorflow import keras
import numpy as np
from .emotion_graph import EmotionGraph

class EmotionalStabilityModel:
    def __init__(self, input_shape, emotion_graph: EmotionGraph, emotional_state, lstm_units=32):
        self.emotion_graph = emotion_graph
        self.emotional_state = emotional_state
        self.num_features = len(emotional_state.emotions) + len(emotion_graph.emotions) * (len(emotion_graph.emotions) - 1)
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Input(shape=input_shape))
        self.model.add(keras.layers.LSTM(lstm_units, input_shape=input_shape))
        self.model.add(keras.layers.Dense(1, activation='sigmoid'))
        self.model.compile(loss='mse', optimizer='adam')

    def predict_emotional_stability(self, input_data):
        prediction = self.model.predict(input_data) 
        return prediction[0][0]

    def train(self, X_train, y_train, epochs=100, batch_size=32):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def prepare_data(self, emotional_history):
        X = []
        y = []
        for i in range(len(emotional_history) - 5):
            #  Создаем  вектор  признаков  для  каждого  шага  времени
            features = []

            #  1.  Добавляем  вектор  эмоционального  состояния
            features.extend(emotional_history[i+5])

            #  2.  Добавляем  информацию  из  EmotionGraph
            for emotion1 in self.emotion_graph.emotions:
                for emotion2 in self.emotion_graph.emotions:
                    if emotion1 != emotion2:
                        influence = self.emotion_graph.get_influence(emotion1, emotion2)
                        emotion1_intensity = emotional_history[i+5][self.emotional_state.emotions.index(emotion1)]
                        features.append(influence * emotion1_intensity)

            X.append(features)
            y.append(emotional_history[i + 5][0])

        #  Преобразуем  X  в  нужную  форму
        X = np.array(X).reshape(20, 1, self.num_features) 
        return X, np.array(y)