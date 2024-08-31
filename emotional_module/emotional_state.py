import numpy as np

class EmotionalState:
    def __init__(self, size=5):
        self.size = size
        self.vector = np.zeros(size)

    def set_emotion_intensity(self, emotion_index, intensity):
        if 0 <= emotion_index < self.size:
            self.vector[emotion_index] = intensity
        else:
            raise ValueError("Invalid emotion index")

    def get_emotion_intensity(self, emotion_index):
        if 0 <= emotion_index < self.size:
            return self.vector[emotion_index]
        else:
            raise ValueError("Invalid emotion index")

    def get_vector(self):
        return self.vector