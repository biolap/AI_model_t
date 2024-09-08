import numpy as np

def calculate_reward(action, emotional_state, emotion_graph):
    """  Рассчитывает  вознаграждение  на  основе  действия  и  эмоционального  состояния.  

    Args:
        action:  Индекс  выбранного  действия.
        emotional_state:  Экземпляр  класса  EmotionalState.
        emotion_graph:  Экземпляр  класса  EmotionGraph.

    Returns:
        Вознаграждение  (число).
    """
    reward = 0
    dominant_emotion_index = np.argmax(emotional_state.get_vector())

    #  1.  Вознаграждение  пропорционально  интенсивности  соответствующей  эмоции
    if  action == 0:  #  Выразить  радость
        reward = emotional_state.get_emotion_intensity(0)
    elif  action == 1:  #  Проявить  грусть
        reward = emotional_state.get_emotion_intensity(1)
    # ... (аналогично  для  других  действий)

    #  2.  Наказание  за  несоответствие  действия  и  доминирующей  эмоции
    if  action != dominant_emotion_index:
        reward -= 0.5

    #  3.  Учет  влияния  EmotionGraph  (пример)
    if  action == 3  and  emotion_graph.get_influence("anger", "fear") > 0.5  and  emotional_state.get_emotion_intensity(2) > 0.6:
        #  Дополнительное  вознаграждение  за  избегание  опасности,  если  гнев  усиливает  страх  и  гнев  высокий
        reward += 0.2

    return  reward