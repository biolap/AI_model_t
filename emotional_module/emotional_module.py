from universal_system import UniversalSystem
from emotional_module.joy_model import JoyModel
from emotional_module.sadness_model import SadnessModel  #  Добавлен  импорт
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
        self.sadness_model = SadnessModel(emotional_state)  #  Добавлен  экземпляр  SadnessModel
        self.anger_model = AngerModel(emotional_state)
        self.fear_model = FearModel(emotional_state)
        self.surprise_model = SurpriseModel(emotional_state)

    def process_stimulus(self, stimulus_intensity, stimulus_valence):
        """  Обрабатывает  внешний  стимул.  """
        #  Обновите  интенсивность  каждой  эмоции
        self.joy_model.simulations["joy"].input['stimulus_intensity'] = stimulus_intensity
        self.joy_model.simulations["joy"].input['stimulus_valence'] = stimulus_valence
        self.joy_model.calculate_intensity("joy", "joy_intensity")  #  Вызываем  через  self.joy_model
        
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

        #  Обновите  EmotionGraph
        self.update_emotion_graph()

    def update_emotion_graph(self):
        """  Обновляет  влияние  эмоций  друг  на  друга.  """
        #  Используйте  self.emotion_graph  и  self.emotional_state  для  вычисления  влияния
        # ... 

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