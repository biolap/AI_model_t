# import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from universal_system import UniversalSystem

# Класс для радости (Joy)
class JoyModel(EmotionModel):
    def __init__(self, emotional_state):
        super().__init__(emotional_state, "joy", 'joy_intensity')
    def define_rules(self):
        return [
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['high']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['medium']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['neutral'], self.intensity['low'])
        ]
# Класс для грусти (Sadness)
class SadnessModel(EmotionModel):
    def __init__(self, emotional_state):
        super().__init__(emotional_state, "sadness", 'sadness_intensity')

    def define_rules(self):
        return [
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['high']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['medium']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['neutral'], self.intensity['low']) 
        ]
# Класс для гнева (Anger)
class AngerModel(EmotionModel):
    def __init__(self, emotional_state):
        super().__init__(emotional_state, "anger", 'anger_intensity')

    def define_rules(self):
        return [
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['high']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['medium']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['neutral'], self.intensity['low'])
        ]

# Класс для страха (Fear)
class FearModel(EmotionModel):
    def __init__(self, emotional_state):
        super().__init__(emotional_state, "fear", 'fear_intensity')

    def define_rules(self):
        return [
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['high']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['medium']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['neutral'], self.intensity['low'])
        ]

# Класс для удивления (Surprise)
class SurpriseModel(EmotionModel):
    def __init__(self, emotional_state):
        super().__init__(emotional_state, "surprise", 'surprise_intensity')

    def define_rules(self):
        return [
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['neutral'], self.intensity['high']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['neutral'], self.intensity['medium']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['neutral'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['low']),
            ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['low'])
        ]