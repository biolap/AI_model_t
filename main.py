import numpy as np

from emotional_module.temperament_model import TemperamentModel
from emotional_module.emotional_stability_model import EmotionalStabilityModel
from emotional_module.emotional_state import EmotionalState
from emotional_module.stimulus_model import StimulusModel
from emotional_module.environment_model import EnvironmentModel
from emotional_module.emotional_module import EmotionalModule
from emotional_module.emotion_graph import EmotionGraph

#  Параметры  для  TemperamentModel
state_size = 3
action_size = 6
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1

#  Создание  экземпляров
emotional_state = EmotionalState()
emotion_graph = EmotionGraph()
temperament_model = TemperamentModel(state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state)
emotional_stability_model = EmotionalStabilityModel(input_shape=(5, 5), emotion_graph=emotion_graph, lstm_units=32)
stimulus_model = StimulusModel()
environment_model = EnvironmentModel()

#  Создаем  экземпляр  EmotionalModule
emotional_module = EmotionalModule(emotional_state)

#  Пример  взаимодействия
    #  1.  Получение  стимула  (задаем  вручную)
stimulus_intensity = 0.8
stimulus_valence = 0.6
for _ in range(25):  #  Цикл  для  создания  25  эмоциональных  состояний
    #  Устанавливаем  стимул
    stimulus_model.set_stimulus(stimulus_intensity,  stimulus_valence)

    #  Устанавливаем  параметры  среды
    environment_model.set_safety("safe")
    environment_model.set_stimulation("high")

    # 2.  EmotionalModule  обрабатывает  стимул  
    emotional_module.process_stimulus(stimulus_intensity,  stimulus_valence)

    #  Обновляем  историю  эмоциональных  состояний
    emotional_state.update_history()

# 3.  Взаимодействие  с  TemperamentModel
current_state = [0.5,  0.2,  1] 
action = temperament_model.get_action(current_state)

# 4.  Взаимодействие  с  EmotionalStabilityModel
emotional_history = emotional_state.get_history() 
emotional_history = np.array(emotional_history).reshape(5, 5, 5)  #  Исправленная  форма
emotional_stability = emotional_stability_model.predict_emotional_stability(emotional_history)

# 5.  Моделирование  изменения  эмоций  со  временем  
time_step = 0.1
emotional_module.evolve(time_step)

#  Вывод  результатов
print(f"Вектор  эмоционального  состояния:  {emotional_state.get_vector()}")
print(f"Выбранное  действие:  {action}")
print(f"Эмоциональная  устойчивость:  {emotional_stability}")
# ...