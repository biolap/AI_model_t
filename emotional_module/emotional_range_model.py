import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class EmotionModel:
    def __init__(self, emotional_state, emotion_name, intensity_name):
        self.emotional_state = emotional_state
        self.emotion_name = emotion_name
        self.intensity_name = intensity_name
        
        self.stimulus_intensity = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'stimulus_intensity')
        self.stimulus_valence = ctrl.Antecedent(np.arange(-1, 1.1, 0.1), 'stimulus_valence')
        
        
        self.intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), intensity_name)
        # Определение fuzzy-множеств (membership functions)
        for var in [self.stimulus_intensity, self.stimulus_valence]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.5])
            var['medium'] = fuzz.trimf(var.universe, [0.25, 0.5, 0.75])
            var['high'] = fuzz.trimf(var.universe, [0.5, 1, 1])

        self.intensity['low'] = fuzz.trimf(self.intensity.universe, [0, 0, 0.5])
        self.intensity['medium'] = fuzz.trimf(self.intensity.universe, [0.25, 0.5, 0.75])
        self.intensity['high'] = fuzz.trimf(self.intensity.universe, [0.5, 1, 1])

        self.stimulus_valence['negative'] = fuzz.trimf(self.stimulus_valence.universe, [-1, -1, 0])
        self.stimulus_valence['neutral'] = fuzz.trimf(self.stimulus_valence.universe, [-0.5, 0, 0.5])
        self.stimulus_valence['positive'] = fuzz.trimf(self.stimulus_valence.universe, [0, 1, 1])
    def get_emotion_intensity(self, stimulus_intensity, stimulus_valence):
        # Определение правил fuzzy logic
        rules = self.define_rules()   
        # Создание системы управления и симуляции
        control_system = ctrl.ControlSystem(rules)
        simulation = ctrl.ControlSystemSimulation(control_system)
        simulation.input['stimulus_intensity'] = stimulus_intensity
        simulation.input['stimulus_valence'] = stimulus_valence        
        # Устанавливаем все выходные переменные в 0.0
        simulation.output['joy_intensity'] = 0.0
        simulation.output['sadness_intensity'] = 0.0
        simulation.output['anger_intensity'] = 0.0
        simulation.output['fear_intensity'] = 0.0
        simulation.output['surprise_intensity'] = 0.0
        simulation.compute()
        intensity = simulation.output[self.intensity_name]
        self.emotional_state.set_emotion_intensity(self.emotional_state.emotions.index(self.emotion_name), intensity)
        return intensity
    def define_rules(self):
        raise NotImplementedError

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