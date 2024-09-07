import numpy as np

class EmotionalState:
    def __init__(self, size=6, intensity=0):
        self.size = size
        self.vector = np.zeros(size)
        self.emotions = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
        self.history = [] 
        #  Устанавливаем  начальную  интенсивность  для  "joy"  
        self.set_emotion_intensity(self.emotions.index("joy"),  intensity)

    def set_emotion_intensity(self, emotion_index, intensity):
        if 0 <= emotion_index < self.size:
            self.vector[emotion_index] = intensity
            print(f"Установка  интенсивности  для  индекса  {emotion_index}  (эмоция:  {self.emotions[emotion_index]}):  {intensity}")
        else:
            raise ValueError("Invalid emotion index")

    def get_emotion_intensity(self, emotion_index):
        if 0 <= emotion_index < self.size:
            return self.vector[emotion_index]
        else:
            raise ValueError("Invalid emotion index")

    def get_vector(self):
        return self.vector

    def get_history(self):
        """ Возвращает историю эмоциональных состояний. """
        return self.history

    def update_history(self):
        """ Добавляет текущее состояние в историю. """
        self.history.append(self.vector.copy())