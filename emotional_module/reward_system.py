import numpy as np

def calculate_reward(action, emotional_state, emotion_graph):
    """ Рассчитывает вознаграждение на основе действия и эмоционального состояния.

    Args:
        action: Индекс выбранного действия.
        emotional_state: Экземпляр класса EmotionalState.
        emotion_graph: Экземпляр класса EmotionGraph.

    Returns:
        Вознаграждение (число).
    """
    reward = 0
    dominant_emotion_index = np.argmax(emotional_state.get_vector())
    emotions = emotional_state.emotions  #  Список  эмоций

    #  1.  Вознаграждение  пропорционально  интенсивности  соответствующей  эмоции
    if action == 0:  # Выразить радость
        reward = emotional_state.get_emotion_intensity(0)
    elif action == 1:  # Проявить грусть
        sadness_intensity = emotional_state.get_emotion_intensity(1)
        reward = sadness_intensity if sadness_intensity > 0.6 else -0.2 
    elif action == 2:  # Проявить гнев
        anger_intensity = emotional_state.get_emotion_intensity(2)
        reward = anger_intensity if anger_intensity > 0.6 else -0.2
    elif action == 3:  # Избегать опасности
        fear_intensity = emotional_state.get_emotion_intensity(3)
        reward = fear_intensity if fear_intensity > 0.6 else -0.2
    elif action == 4:  # Взаимодействовать с объектом
        surprise_intensity = emotional_state.get_emotion_intensity(4)
        reward = surprise_intensity if surprise_intensity > 0.6 else -0.2
    elif action == 5:  # Не выражать эмоций
        disgust_intensity = emotional_state.get_emotion_intensity(5)
        reward = disgust_intensity if disgust_intensity > 0.6 else -0.2
            
    #  2.  Наказание  за  несоответствие  действия  и  доминирующей  эмоции
    if action != dominant_emotion_index:
        reward -= 0.5

    #  3.  Учет  влияния  EmotionGraph  (пример)
    if action == 3 and emotion_graph.get_influence("anger", "fear") > 0.5 and emotional_state.get_emotion_intensity(2) > 0.6:
        reward += 0.2

    return reward