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

        # Определение fuzzy-множеств (membership functions)
        for var in [self.stimulus_intensity, self.stimulus_valence]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.5])
            var['medium'] = fuzz.trimf(var.universe, [0.25, 0.5, 0.75])
            var['high'] = fuzz.trimf(var.universe, [0.5, 1, 1])

        for emotion_intensity in [self.joy_intensity, self.sadness_intensity]:
            emotion_intensity['low'] = fuzz.trimf(emotion_intensity.universe, [0, 0, 0.5])
            emotion_intensity['medium'] = fuzz.trimf(emotion_intensity.universe, [0.25, 0.5, 0.75])
            emotion_intensity['high'] = fuzz.trimf(emotion_intensity.universe, [0.5, 1, 1])

        self.stimulus_valence['negative'] = fuzz.trimf(self.stimulus_valence.universe, [-1, -1, 0])
        self.stimulus_valence['neutral'] = fuzz.trimf(self.stimulus_valence.universe, [-0.5, 0, 0.5])
        self.stimulus_valence['positive'] = fuzz.trimf(self.stimulus_valence.universe, [0, 1, 1])

        # Определение правил fuzzy logic
        self.rules = {
            "joy": [
                ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.joy_intensity['high']),
                ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.joy_intensity['medium']),
                ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.joy_intensity['low'])
            ],
            "sadness": [
                ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.sadness_intensity['high']),
                ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.sadness_intensity['medium']),
                ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.sadness_intensity['low'])
            ]
            #  ... (добавьте правила для других эмоций позже) 
        }

        # Создание систем управления и симуляций
        self.simulations = {}
        for emotion, rules in self.rules.items():
            #  Создаем симуляцию только для текущей эмоции
            self.simulations[emotion] = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

        # EmotionalState
        self.emotional_state = emotional_state

    def get_emotion_intensity(self, emotion, stimulus_intensity, stimulus_valence):
        if emotion not in self.simulations:
            raise ValueError(f"Invalid emotion: {emotion}")

        simulation = self.simulations[emotion]  #  Получаем симуляцию для нужной эмоции
        simulation.input['stimulus_intensity'] = stimulus_intensity
        simulation.input['stimulus_valence'] = stimulus_valence
        simulation.compute()

        intensity = simulation.output[f'{emotion}_intensity']

        #  Используем правильный индекс для каждой эмоции
        if emotion == "joy":
            self.emotional_state.set_emotion_intensity(0, intensity)  
        elif emotion == "sadness":
            self.emotional_state.set_emotion_intensity(1, intensity) 

        return intensity


# class EmotionalRangeModel:
#     def __init__(self, emotional_state):
#         # Определение fuzzy-переменных
#         self.stimulus_intensity = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'stimulus_intensity')
#         self.stimulus_valence = ctrl.Antecedent(np.arange(-1, 1.1, 0.1), 'stimulus_valence')

#         self.joy_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'joy_intensity')
#         self.sadness_intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'sadness_intensity')

#         # Определение fuzzy-множеств (membership functions)
#         for var in [self.stimulus_intensity, self.stimulus_valence]:
#             var['low'] = fuzz.trimf(var.universe, [0, 0, 0.5])
#             var['medium'] = fuzz.trimf(var.universe, [0.25, 0.5, 0.75])
#             var['high'] = fuzz.trimf(var.universe, [0.5, 1, 1])

#         self.joy_intensity['low'] = fuzz.trimf(self.joy_intensity.universe, [0, 0, 0.5])  #  Fuzzy-множества для joy_intensity
#         self.joy_intensity['medium'] = fuzz.trimf(self.joy_intensity.universe, [0.25, 0.5, 0.75])
#         self.joy_intensity['high'] = fuzz.trimf(self.joy_intensity.universe, [0.5, 1, 1])
        
#         self.sadness_intensity['low'] = fuzz.trimf(self.sadness_intensity.universe, [0, 0, 0.5])
#         self.sadness_intensity['medium'] = fuzz.trimf(self.sadness_intensity.universe, [0.25, 0.5, 0.75])
#         self.sadness_intensity['high'] = fuzz.trimf(self.sadness_intensity.universe, [0.5, 1, 1])

#         self.stimulus_valence['negative'] = fuzz.trimf(self.stimulus_valence.universe, [-1, -1, 0])
#         self.stimulus_valence['neutral'] = fuzz.trimf(self.stimulus_valence.universe, [-0.5, 0, 0.5])
#         self.stimulus_valence['positive'] = fuzz.trimf(self.stimulus_valence.universe, [0, 1, 1])

#         # Определение правил fuzzy logic (только для радости)
#         self.rule1_joy = ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.joy_intensity['high'])
#         self.rule2_joy = ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.joy_intensity['medium'])
#         self.rule3_joy = ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.joy_intensity['low'])
        
#         self.rule1_sadness = ctrl.Rule(self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.sadness_intensity['high'])
#         self.rule2_sadness = ctrl.Rule(self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.sadness_intensity['medium'])
#         self.rule3_sadness = ctrl.Rule(self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.sadness_intensity['low'])

#         # Создание системы управления и симуляции (только для радости)
#         joy_control_system = ctrl.ControlSystem([self.rule1_joy, self.rule2_joy, self.rule3_joy])
#         self.joy_simulation = ctrl.ControlSystemSimulation(joy_control_system)
        
#         # Система управления и симуляция для sadness
#         sadness_control_system = ctrl.ControlSystem([self.rule1_sadness, self.rule2_sadness, self.rule3_sadness])
#         self.sadness_simulation = ctrl.ControlSystemSimulation(sadness_control_system)

#         # EmotionalState
#         self.emotional_state = emotional_state

    # def get_emotion_intensity(self, emotion, stimulus_intensity, stimulus_valence):
    #     if emotion != "joy":  # Проверяем,  что запрашивается радость
    #         raise ValueError(f"Invalid emotion: {emotion},  only 'joy' is supported at this stage.")

    #     self.joy_simulation.input['stimulus_intensity'] = stimulus_intensity
    #     self.joy_simulation.input['stimulus_valence'] = stimulus_valence
    #     self.joy_simulation.compute()

    #     intensity = self.joy_simulation.output['joy_intensity']
    #     self.emotional_state.set_emotion_intensity(0, intensity)  # Обновляем EmotionalState
    #     return intensity
    
    # def get_emotion_intensity(self, emotion, stimulus_intensity, stimulus_valence):
    #     if emotion == "joy":
    #         self.joy_simulation.input['stimulus_intensity'] = stimulus_intensity
    #         self.joy_simulation.input['stimulus_valence'] = stimulus_valence
    #         self.joy_simulation.compute()

    #         intensity = self.joy_simulation.output['joy_intensity']
    #         self.emotional_state.set_emotion_intensity(0, intensity)  
    #         return intensity

    #     elif emotion == "sadness":
    #         self.sadness_simulation.input['stimulus_intensity'] = stimulus_intensity
    #         self.sadness_simulation.input['stimulus_valence'] = stimulus_valence
    #         self.sadness_simulation.compute()

    #         intensity = self.sadness_simulation.output['sadness_intensity']
    #         self.emotional_state.set_emotion_intensity(1, intensity)  
    #         return intensity

    #     else:
    #         raise ValueError(f"Invalid emotion: {emotion}, only 'joy' and 'sadness' are supported at this stage.")