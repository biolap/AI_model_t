from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

emotional_history = [
    [0.8, 0.2, 0.3, 0.1, 0.6],  # Состояние 1
    [0.7, 0.3, 0.2, 0.2, 0.5],  # Состояние 2
    [0.6, 0.4, 0.1, 0.3, 0.4],  # Состояние 3
    [0.5, 0.5, 0.0, 0.4, 0.3],  # Состояние 4
    [0.4, 0.6, 0.1, 0.5, 0.2],  # Состояние 5
    [0.3, 0.7, 0.2, 0.6, 0.1],  # Состояние 6
    [0.2, 0.8, 0.3, 0.7, 0.0],  # Состояние 7
    [0.1, 0.9, 0.4, 0.8, 0.1],  # Состояние 8
    [0.0, 1.0, 0.5, 0.9, 0.2],  # Состояние 9
    [0.1, 0.9, 0.6, 0.8, 0.3],  # Состояние 10
    [0.2, 0.8, 0.7, 0.7, 0.4],  # Состояние 11
    [0.3, 0.7, 0.8, 0.6, 0.5],  # Состояние 12
    [0.4, 0.6, 0.9, 0.5, 0.6],  # Состояние 13
    [0.5, 0.5, 1.0, 0.4, 0.7],  # Состояние 14
    [0.6, 0.4, 0.9, 0.3, 0.8],  # Состояние 15
    [0.7, 0.3, 0.8, 0.2, 0.9],  # Состояние 16
    [0.8, 0.2, 0.7, 0.1, 1.0],  # Состояние 17
    [0.9, 0.1, 0.6, 0.0, 0.9],  # Состояние 18
    [1.0, 0.0, 0.5, 0.1, 0.8],  # Состояние 19
    [0.9, 0.1, 0.4, 0.2, 0.7],  # Состояние 20
]

class EmotionalStabilityModel:
    def __init__(self, input_shape, lstm_units=32):
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Input(shape=input_shape)) # Добавляем Input слой
        self.model.add(keras.layers.LSTM(lstm_units))
        self.model.add(keras.layers.Dense(1, activation='sigmoid')) 
        self.model.compile(loss='mse', optimizer='adam')    
    def predict_emotional_stability(self, input_data):
        # Преобразование input_data в формат,  подходящий для LSTM (batch_size, timesteps, features)
        # ... 
        prediction = self.model.predict(input_data)
        return prediction[0][0] # Возвращаем  значение от 0 до 1

    def train(self, X_train, y_train, epochs=100, batch_size=32):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    def prepare_data(self, emotional_history):
        X = []
        y = []
        for i in range(len(emotional_history) - 5):  # 5 - timesteps
            X.append(emotional_history[i:i+5])  # Берем 5 последних состояний
            y.append(emotional_history[i+5][0])  # Берем значение радости из следующего состояния (индекс 0)

        return np.array(X), np.array(y)
# Создание обучающих данных
input_shape = (5, 5)  # timesteps=5, features=5
lstm_units = 32
model = EmotionalStabilityModel(input_shape, lstm_units)
X_train, y_train = model.prepare_data(emotional_history)

# Обучение модели
model.train(X_train, y_train, epochs=100, batch_size=32)

# Визуализация
plt.plot(y_train, color='blue', label='Реальная эмоциональная устойчивость')
plt.plot(model.predict_emotional_stability(X_train), color='red', label='Предсказанная эмоциональная устойчивость')
plt.xlabel('Время')
plt.ylabel('Эмоциональная устойчивость')
plt.legend()
plt.show()