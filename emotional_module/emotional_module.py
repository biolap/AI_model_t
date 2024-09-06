from universal_system import UniversalSystem
from emotional_module.joy_model import JoyModel
from emotional_module.sadness_model import SadnessModel
from emotional_module.disgust_model import DisgustModel
from emotional_module.anger_model import AngerModel
from emotional_module.fear_model import FearModel
from emotional_module.surprise_model import SurpriseModel
from emotional_module.emotion_graph import EmotionGraph


class EmotionalModule(UniversalSystem):
    def __init__(self, emotional_state):
        super().__init__("EmotionalModule", emotional_state)
        self.emotional_state = emotional_state
        self.emotion_graph = EmotionGraph()

        #  Создайте  экземпляры  моделей  эмоций
        self.joy_model = JoyModel(emotional_state)
        self.sadness_model = SadnessModel(emotional_state)
        self.anger_model = AngerModel(emotional_state)
        self.fear_model = FearModel(emotional_state)
        self.surprise_model = SurpriseModel(emotional_state)
        self.disgust_model = DisgustModel(emotional_state)

    def process_stimulus(self, stimulus_intensity, stimulus_valence):
        """  Обрабатывает  внешний  стимул.  """
        #  Обновите  интенсивность  каждой  эмоции
        self.joy_model.simulations["joy"].input['stimulus_intensity'] = stimulus_intensity
        self.joy_model.simulations["joy"].input['stimulus_valence'] = stimulus_valence
        self.joy_model.calculate_intensity("joy", "joy_intensity")
        
        self.sadness_model.simulations["sadness"].input['stimulus_intensity'] = stimulus_intensity
        self.sadness_model.simulations["sadness"].input['stimulus_valence'] = stimulus_valence
        self.sadness_model.calculate_intensity("sadness", "sadness_intensity")
        
        self.anger_model.simulations["anger"].input['stimulus_intensity'] = stimulus_intensity
        self.anger_model.simulations["anger"].input['stimulus_valence'] = stimulus_valence
        self.anger_model.calculate_intensity("anger", "anger_intensity")

        self.fear_model.simulations["fear"].input['stimulus_intensity'] = stimulus_intensity
        self.fear_model.simulations["fear"].input['stimulus_valence'] = stimulus_valence
        self.fear_model.calculate_intensity("fear", "fear_intensity")

        self.surprise_model.simulations["surprise"].input['stimulus_intensity'] = stimulus_intensity
        self.surprise_model.simulations["surprise"].input['stimulus_valence'] = stimulus_valence
        self.surprise_model.calculate_intensity("surprise", "surprise_intensity")
        
        self.disgust_model.simulations["disgust"].input['stimulus_intensity'] = stimulus_intensity
        self.disgust_model.simulations["disgust"].input['stimulus_valence'] = stimulus_valence
        self.disgust_model.calculate_intensity("disgust", "disgust_intensity")

        #  Обновите  EmotionGraph
        self.update_emotion_graph()

    def update_emotion_graph(self):
        """  Обновляет  влияние  эмоций  друг  на  друга.  """
        for i, emotion1 in enumerate(self.emotion_graph.emotions):
            for j, emotion2 in enumerate(self.emotion_graph.emotions):
                if i != j:  #  Не  учитываем  влияние  эмоции  на  саму  себя
                    influence = self.emotion_graph.get_influence(emotion1, emotion2)
                    emotion1_intensity = self.emotional_state.get_emotion_intensity(i)
                    influence_effect = influence * emotion1_intensity
                    current_emotion2_intensity = self.emotional_state.get_emotion_intensity(j)
                    new_emotion2_intensity = current_emotion2_intensity + influence_effect

                    #  Убедимся,  что  интенсивность  остается  в  пределах  0-1
                    new_emotion2_intensity = max(0.0, min(new_emotion2_intensity, 1.0))
                    
                    # print(f"Влияние  {emotion1}  на  {emotion2}:  {influence_effect:.2f}")  #  Отладочный  вывод
                    # print(f"Старая  интенсивность  {emotion2}:  {current_emotion2_intensity:.2f}")  #  Отладочный  вывод
                    # print(f"Новая  интенсивность  {emotion2}:  {new_emotion2_intensity:.2f}\n")  #  Отладочный  вывод
                    
                    self.emotional_state.set_emotion_intensity(j, new_emotion2_intensity)

    def interact_with_other_modules(self, other_module):
        """  Взаимодействует  с  другими  модулями.  """
        #  Определите,  как  EmotionalModule  взаимодействует  с  другими  модулями
        #  (например,  TemperamentModel,  EmotionalStabilityModel,  Memory)
        # ...

    def evolve(self, time_step):
        """  Моделирует  изменение  эмоций  со  временем.  """
        self.joy_model.evolve(time_step)
        self.sadness_model.evolve(time_step)  
        self.anger_model.evolve(time_step)  
        self.fear_model.evolve(time_step)  
        self.surprise_model.evolve(time_step)
        self.disgust_model.evolve(time_step)