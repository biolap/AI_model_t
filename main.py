import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from emotional_module.temperament_model import TemperamentModel
from emotional_module.emotional_stability_model import EmotionalStabilityModel
from emotional_module.emotional_state import EmotionalState
from emotional_module.emotion_graph import EmotionGraph
from emotional_module.emotional_range_model import JoyModel, SadnessModel

# Параметры для TemperamentModel
state_size = 3
action_size = 6
learning_rate = 0.1
discount_factor = 0.9
epsilon = 0.1

# Создание экземпляров
emotional_state = EmotionalState()
joy_model = JoyModel(emotional_state)  #  Создаем экземпляр JoyModel
sadness_model = SadnessModel(emotional_state)  #  Создаем экземпляр SadnessModel
temperament_model = TemperamentModel(state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state)
emotional_stability_model = EmotionalStabilityModel(input_shape=(5, 5), lstm_units=32)
emotion_graph = EmotionGraph()

def visualize_emotion_graph(emotion_graph, emotional_state):
    """Визуализирует граф эмоций.

    Args:
        emotion_graph: Экземпляр класса EmotionGraph.
        emotional_state: Экземпляр класса EmotionalState.
    """
    # Получаем интенсивность эмоций из emotional_state
    emotion_intensities = {
        emotion: emotional_state.get_emotion_intensity(i) 
        for i, emotion in enumerate(emotion_graph.emotions)
    }

    # Создаем макет графа
    pos = nx.spring_layout(emotion_graph.graph)

    # Рисуем узлы с размером,  пропорциональным интенсивности эмоции
    node_sizes = [intensity * 1000 for intensity in emotion_intensities.values()]
    nx.draw_networkx_nodes(emotion_graph.graph, pos, node_size=node_sizes, node_color="lightblue")

    # Рисуем ребра с толщиной,  пропорциональной весу
    edge_widths = [data['weight'] * 5 for _, _, data in emotion_graph.graph.edges(data=True)]
    nx.draw_networkx_edges(emotion_graph.graph, pos, width=edge_widths, edge_color="gray")

    # Добавляем метки к узлам
    nx.draw_networkx_labels(emotion_graph.graph, pos, font_size=10)

    # Отображаем граф
    plt.title("Граф эмоций")
    plt.axis('off')
    plt.show()

# Пример взаимодействия
# 1. Получение стимула (задаем вручную)
stimulus_intensity = 0.8 
stimulus_valence = -0.6

# 2. Вычисление интенсивности эмоций
joy_intensity = joy_model.get_emotion_intensity(stimulus_intensity, stimulus_valence)  #  Используем joy_model
sadness_intensity = sadness_model.get_emotion_intensity(stimulus_intensity, stimulus_valence)  #  Используем sadness_model

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
print(f"Интенсивность грусти: {sadness_intensity}")  # Выводим sadness

# ... (вывод для других эмоций)
print(f"Выбранное действие: {action}")
print(f"Эмоциональная устойчивость: {emotional_stability}")
print(f"Влияние радости на страх: {joy_influence_on_fear}")

# Визуализация
visualize_emotion_graph(emotion_graph, emotional_state)