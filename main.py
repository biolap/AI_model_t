import numpy as np

from emotional_module.temperament_model import TemperamentModel
from emotional_module.emotional_range_model import EmotionalRangeModel
from emotional_module.emotional_stability_model import EmotionalStabilityModel
from emotional_module.emotional_state import EmotionalState
from emotional_module.emotion_graph import EmotionGraph

# Параметры для TemperamentModel
state_size = 3
action_size = 6
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1

# Создание экземпляров
emotional_state = EmotionalState()
temperament_model = TemperamentModel(state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state)
emotional_range_model = EmotionalRangeModel(emotional_state)
emotional_stability_model = EmotionalStabilityModel(input_shape=(5, 5), lstm_units=32)
emotion_graph = EmotionGraph()

# Пример взаимодействия
# 1. Получение стимула (задаем вручную)
stimulus_intensity = 0.8 
stimulus_valence = 0.6

# 2. EmotionalRangeModel обрабатывает стимул
joy_intensity = emotional_range_model.get_emotion_intensity("joy", stimulus_intensity, stimulus_valence)
sadness_intensity = emotional_range_model.get_emotion_intensity("sadness", stimulus_intensity, stimulus_valence)
anger_intensity = emotional_range_model.get_emotion_intensity("anger", stimulus_intensity, stimulus_valence)
fear_intensity = emotional_range_model.get_emotion_intensity("fear", stimulus_intensity, stimulus_valence)
surprise_intensity = emotional_range_model.get_emotion_intensity("surprise", stimulus_intensity, stimulus_valence)

# 3. TemperamentModel выбирает действие (задаем состояние вручную)
current_state = [0.5, 0.2, 1]  # Пример вектора состояния
action = temperament_model.get_action(current_state)

# 4. EmotionalStabilityModel предсказывает устойчивость (задаем историю состояний вручную)
emotional_history = [
    [0.8, 0.2, 0.3, 0.1, 0.6],
    [0.7, 0.3, 0.2, 0.2, 0.5],
    [0.6, 0.4, 0.1, 0.3, 0.4],
    [0.5, 0.5, 0.0, 0.4, 0.3],
    [0.4, 0.6, 0.1, 0.5, 0.2],
]
emotional_stability = emotional_stability_model.predict_emotional_stability(np.array([emotional_history]))
# 5. EmotionGraph определяет влияние эмоций
joy_influence_on_fear = emotion_graph.get_influence("joy", "fear")

# Вывод результатов
print(f"Вектор эмоционального состояния: {emotional_state.get_vector()}")
print(f"Интенсивность радости: {joy_intensity}")
print(f"Интенсивность грусти: {sadness_intensity}")
print(f"Интенсивность гнева: {anger_intensity}")
print(f"Интенсивность страха: {fear_intensity}")
print(f"Интенсивность удивления: {surprise_intensity}")
print(f"Выбранное действие: {action}")
print(f"Эмоциональная устойчивость: {emotional_stability}")
print(f"Влияние радости на страх: {joy_influence_on_fear}")