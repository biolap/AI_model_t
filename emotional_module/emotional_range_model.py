import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class EmotionalRangeModel:
    def __init__(self, emotional_state):
        # Определение fuzzy-переменных
        self.stimulus_intensity = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'stimulus_intensity')
        self.stimulus_valence = ctrl.Antecedent(np.arange(-1, 1.1, 0.1), 'stimulus_valence')
        self.joy_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'joy_intensity')
        self.sadness_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'sadness_intensity')
        self.anger_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'anger_intensity')
        self.fear_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'fear_intensity')
        self.surprise_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'surprise_intensity')

        # Определение fuzzy-множеств (membership functions)
        self.stimulus_intensity['низкая'] = fuzz.trimf(self.stimulus_intensity.universe, [0, 0, 0.5])
        self.stimulus_intensity['средняя'] = fuzz.trimf(self.stimulus_intensity.universe, [0.25, 0.5, 0.75])
        self.stimulus_intensity['высокая'] = fuzz.trimf(self.stimulus_intensity.universe, [0.5, 1, 1])

        self.stimulus_valence['отрицательная'] = fuzz.trimf(self.stimulus_valence.universe, [-1, -1, 0])
        self.stimulus_valence['нейтральная'] = fuzz.trimf(self.stimulus_valence.universe, [-0.5, 0, 0.5])
        self.stimulus_valence['положительная'] = fuzz.trimf(self.stimulus_valence.universe, [0, 1, 1])

        self.joy_intensity['низкая'] = fuzz.trimf(self.joy_intensity.universe, [0, 0, 0.5])
        self.joy_intensity['средняя'] = fuzz.trimf(self.joy_intensity.universe, [0.25, 0.5, 0.75])
        self.joy_intensity['высокая'] = fuzz.trimf(self.joy_intensity.universe, [0.5, 1, 1])

        self.sadness_intensity['низкая'] = fuzz.trimf(self.sadness_intensity.universe, [0, 0, 0.5])
        self.sadness_intensity['средняя'] = fuzz.trimf(self.sadness_intensity.universe, [0.25, 0.5, 0.75])
        self.sadness_intensity['высокая'] = fuzz.trimf(self.sadness_intensity.universe, [0.5, 1, 1])

        self.anger_intensity['низкая'] = fuzz.trimf(self.anger_intensity.universe, [0, 0, 0.5])
        self.anger_intensity['средняя'] = fuzz.trimf(self.anger_intensity.universe, [0.25, 0.5, 0.75])
        self.anger_intensity['высокая'] = fuzz.trimf(self.anger_intensity.universe, [0.5, 1, 1])

        self.fear_intensity['низкая'] = fuzz.trimf(self.fear_intensity.universe, [0, 0, 0.5])
        self.fear_intensity['средняя'] = fuzz.trimf(self.fear_intensity.universe, [0.25, 0.5, 0.75])
        self.fear_intensity['высокая'] = fuzz.trimf(self.fear_intensity.universe, [0.5, 1, 1])

        self.surprise_intensity['низкая'] = fuzz.trimf(self.surprise_intensity.universe, [0, 0, 0.5])
        self.surprise_intensity['средняя'] = fuzz.trimf(self.surprise_intensity.universe, [0.25, 0.5, 0.75])
        self.surprise_intensity['высокая'] = fuzz.trimf(self.surprise_intensity.universe, [0.5, 1, 1])

        # Определение правил fuzzy logic
        rule1_joy = ctrl.Rule(self.stimulus_intensity['высокая'] & self.stimulus_valence['положительная'], self.joy_intensity['высокая'])
        rule2_joy = ctrl.Rule(self.stimulus_intensity['средняя'] & self.stimulus_valence['положительная'], self.joy_intensity['средняя'])
        rule3_joy = ctrl.Rule(self.stimulus_intensity['низкая'] & self.stimulus_valence['положительная'], self.joy_intensity['низкая'])

        rule1_sadness = ctrl.Rule(self.stimulus_intensity['высокая'] & self.stimulus_valence['отрицательная'], self.sadness_intensity['высокая'])
        rule2_sadness = ctrl.Rule(self.stimulus_intensity['средняя'] & self.stimulus_valence['отрицательная'], self.sadness_intensity['средняя'])
        rule3_sadness = ctrl.Rule(self.stimulus_intensity['низкая'] & self.stimulus_valence['отрицательная'], self.sadness_intensity['низкая'])

        rule1_anger = ctrl.Rule(self.stimulus_intensity['высокая'] & self.stimulus_valence['отрицательная'], self.anger_intensity['высокая'])
        rule2_anger = ctrl.Rule(self.stimulus_intensity['средняя'] & self.stimulus_valence['отрицательная'], self.anger_intensity['средняя'])
        rule3_anger = ctrl.Rule(self.stimulus_intensity['низкая'] & self.stimulus_valence['отрицательная'], self.anger_intensity['низкая'])

        rule1_fear = ctrl.Rule(self.stimulus_intensity['высокая'] & self.stimulus_valence['отрицательная'], self.fear_intensity['высокая'])
        rule2_fear = ctrl.Rule(self.stimulus_intensity['средняя'] & self.stimulus_valence['отрицательная'], self.fear_intensity['средняя'])
        rule3_fear = ctrl.Rule(self.stimulus_intensity['низкая'] & self.stimulus_valence['отрицательная'], self.fear_intensity['низкая'])

        rule1_surprise = ctrl.Rule(self.stimulus_intensity['высокая'] & self.stimulus_valence['нейтральная'], self.surprise_intensity['высокая'])
        rule2_surprise = ctrl.Rule(self.stimulus_intensity['средняя'] & self.stimulus_valence['нейтральная'], self.surprise_intensity['средняя'])
        rule3_surprise = ctrl.Rule(self.stimulus_intensity['низкая'] & self.stimulus_valence['нейтральная'], self.surprise_intensity['низкая'])

        # Создание систем управления
        self.joy_ctrl = ctrl.ControlSystem([rule1_joy, rule2_joy, rule3_joy])
        self.sadness_ctrl = ctrl.ControlSystem([rule1_sadness, rule2_sadness, rule3_sadness])
        self.anger_ctrl = ctrl.ControlSystem([rule1_anger, rule2_anger, rule3_anger])
        self.fear_ctrl = ctrl.ControlSystem([rule1_fear, rule2_fear, rule3_fear])
        self.surprise_ctrl = ctrl.ControlSystem([rule1_surprise, rule2_surprise, rule3_surprise])

        # Создание симуляции системы управления
        self.joy_simulation = ctrl.ControlSystemSimulation(self.joy_ctrl)
        self.joy_simulation.output['joy_intensity'] = 0.0

        self.sadness_simulation = ctrl.ControlSystemSimulation(self.sadness_ctrl)
        self.sadness_simulation.output['sadness_intensity'] = 0.0

        self.anger_simulation = ctrl.ControlSystemSimulation(self.anger_ctrl)
        self.anger_simulation.output['anger_intensity'] = 0.0

        self.fear_simulation = ctrl.ControlSystemSimulation(self.fear_ctrl)
        self.fear_simulation.output['fear_intensity'] = 0.0

        self.surprise_simulation = ctrl.ControlSystemSimulation(self.surprise_ctrl)
        self.surprise_simulation.output['surprise_intensity'] = 0.0

        # EmotionalState
        self.emotional_state = emotional_state

    def get_emotion_intensity(self, emotion, stimulus_intensity, stimulus_valence):
        if emotion == "joy":
            self.joy_simulation.input['stimulus_intensity'] = stimulus_intensity
            self.joy_simulation.input['stimulus_valence'] = stimulus_valence
            
            # Активация выхода
            self.joy_simulation.compute() 
            intensity = self.joy_simulation.output['joy_intensity']
            self.emotional_state.set_emotion_intensity(0, intensity)
            return intensity

        elif emotion == "sadness":
            self.sadness_simulation.input['stimulus_intensity'] = stimulus_intensity
            self.sadness_simulation.input['stimulus_valence'] = stimulus_valence
            
            # Активация выхода
            self.sadness_simulation.compute()
            intensity = self.sadness_simulation.output['sadness_intensity']
            self.emotional_state.set_emotion_intensity(1, intensity)
            return intensity
        elif emotion == "anger":
            self.anger_simulation.input['stimulus_intensity'] = stimulus_intensity
            self.anger_simulation.input['stimulus_valence'] = stimulus_valence
            self.anger_simulation.compute()  # !!! ДОБАВЛЕНО
            intensity = self.anger_simulation.output['anger_intensity']
            self.emotional_state.set_emotion_intensity(2, intensity)
            return intensity
        elif emotion == "fear":
            self.fear_simulation.input['stimulus_intensity'] = stimulus_intensity
            self.fear_simulation.input['stimulus_valence'] = stimulus_valence
            self.fear_simulation.compute()  # !!! ДОБАВЛЕНО
            intensity = self.fear_simulation.output['fear_intensity']
            self.emotional_state.set_emotion_intensity(3, intensity)
            return intensity
        elif emotion == "surprise":
            self.surprise_simulation.input['stimulus_intensity'] = stimulus_intensity
            self.surprise_simulation.input['stimulus_valence'] = stimulus_valence
            self.surprise_simulation.compute()  # !!! ДОБАВЛЕНО
            intensity = self.surprise_simulation.output['surprise_intensity']
            self.emotional_state.set_emotion_intensity(4, intensity)
            return intensity
        else:
            raise ValueError(f"Invalid emotion: {emotion}")