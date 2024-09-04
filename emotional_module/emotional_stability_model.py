from tensorflow import keras
import numpy as np
from .emotion_graph import EmotionGraph
class EmotionalStabilityModel:
    def __init__(self, input_shape, emotion_graph, lstm_units=32):
        self.emotion_graph = emotion_graph
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Input(shape=input_shape))
        self.model.add(keras.layers.LSTM(lstm_units))
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
        for i in range(len(emotional_history) - 5):  # 5 - timesteps
            X.append(emotional_history[i:i+5])
            y.append(emotional_history[i+5][0])  #  Предполагаем,  что  эмоциональная  устойчивость  -  это  первый  элемент  вектора
        return np.array(X), np.array(y)