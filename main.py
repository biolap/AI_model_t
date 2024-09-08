import random
import time
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

#  Спецификация  экспериментальной  модели
experiment_name = "LSTM_2_layers"
lstm_units = 32
epochs = 50
batch_size = 32

#  Создание  файла  результатов
timestamp = time.strftime("%Y%m%d-%H%M%S")
filename = f"results_{experiment_name}_{timestamp}.txt"

#  Создание  экземпляров
emotional_state = EmotionalState()
emotion_graph = EmotionGraph()
temperament_model = TemperamentModel(state_size, action_size, learning_rate, discount_factor, epsilon, emotional_state, emotion_graph)
emotional_stability_model = EmotionalStabilityModel(input_shape=(5, 6), emotion_graph=emotion_graph, emotional_state=emotional_state, lstm_units=lstm_units)
stimulus_model = StimulusModel()
environment_model = EnvironmentModel()
emotional_module = EmotionalModule(emotional_state)

# #  Генерация  обучающих  данных  для  EmotionalStabilityModel
# num_training_samples = 1000  #  Количество  примеров  для  обучения
# X_train, y_train = emotional_stability_model.generate_training_data(num_training_samples)

# #  Разделяем  X_train  на  три  отдельных  массива
# history_train = X_train[:, emotional_state.size:emotional_state.size * 6]  #  Извлекаем  данные  истории  эмоций  
# current_state_train = X_train[:, :emotional_state.size]  #  Извлекаем  данные  текущего  состояния
# graph_weights_train = X_train[:, emotional_state.size * 6:]  #  Извлекаем  данные  графа  эмоций

# #  Преобразуем  данные  в  нужный  формат
# history_train = history_train.reshape((history_train.shape[0], 5, emotional_state.size))
# current_state_train = current_state_train.reshape((current_state_train.shape[0], emotional_state.size))  #  Изменено  
# graph_weights_train = graph_weights_train.reshape((graph_weights_train.shape[0], 6, 6))  #  Изменено 

# #  Обучение  EmotionalStabilityModel
# emotional_stability_model.train([history_train, current_state_train, graph_weights_train], y_train, epochs=epochs, batch_size=batch_size)  

# with open(filename, 'w') as f:
#     #  Запись  заголовков  столбцов
#     f.write("Iteration,Stimulus Intensity,Stimulus Valence,"
#                 "Joy,Sadness,Anger,Fear,Surprise,Disgust,"  #  Добавлены  названия  эмоций
#                 "Action,Emotional Stability,Time\n")

#     #  Запись  описания  действий
#     f.write("Action description:  0 - Выразить  радость,  1 - Проявить  грусть,  2 - Проявить  гнев, "
#                 "3 - Избегать  опасности,  4 - Взаимодействовать  с  объектом,  5 - Не  выражать  эмоций\n")  

# #  Пример  взаимодействия
# for  iteration  in  range(25):  #  25  итераций  для  обучения
#     start_time = time.time()

#     #  1.  Получение  стимула  (случайные  значения)
#     stimulus_intensity = random.uniform(0,  1)
#     stimulus_valence = random.uniform(-1,  1)

#     #  2.  Установка  стимула
#     stimulus_model.set_stimulus(stimulus_intensity,  stimulus_valence)

#     #  3.  EmotionalModule  обрабатывает  стимул
#     emotional_module.process_stimulus(stimulus_intensity,  stimulus_valence)

#     #  4.  Обновление  EmotionGraph
#     emotional_module.update_emotion_graph()

#     #  5.  Обновление  истории  эмоциональных  состояний
#     emotional_state.update_history()

#     #  6.  Взаимодействие  с  TemperamentModel
#     current_state = [0.5,  0.2,  1]  #  Пример  вектора  состояния
#     action = temperament_model.get_action(current_state)

#     #  7.  Определение  вознаграждения  (пример)
#     reward = 0
#     if  action == 0  and  emotional_state.get_emotion_intensity(0)  >  0.8:  #  Выразить  радость,  если  радость  высокая
#         reward = 1
#     elif  action == 3  and  emotional_state.get_emotion_intensity(3)  >  0.8:  #  Избегать  опасности,  если  страх  высокий
#         reward = 1
#     else:
#         reward = -0.1  #  Небольшое  отрицательное  вознаграждение  за  другие  действия

#     #  8.  Обновление  Q-таблицы
#     next_state = [0.6,  0.1,  2]  #  Пример  следующего  состояния (вам  нужно  определить  логику  перехода)
#     next_state = np.clip(next_state,  0,  1)  #  Ограничиваем  значения  диапазоном  [0,  1]
#     temperament_model.update_q_table(current_state,  action,  reward,  next_state)

#     #  9.  Взаимодействие  с  EmotionalStabilityModel  (только  если  есть  достаточно  данных)
#     if  len(emotional_state.get_history())  >=  5:
#         current_emotional_state = emotional_state.get_vector()
#         emotional_history = emotional_state.get_history()[-5:]  #  Последние  5  состояний
#         emotion_graph_weights = emotion_graph.weights
#         emotional_stability = emotional_stability_model.predict_emotional_stability(
#             current_emotional_state,  emotional_history,  emotion_graph_weights
#         )
#     else:
#         emotional_stability = 0.5  #  Значение  по  умолчанию

#     #  10.  Моделирование  изменения  эмоций  со  временем
#     time_step = 0.1
#     emotional_module.evolve(time_step)

#     #  11.  Запись  результатов  в  файл
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     f.write(f"{iteration},{stimulus_intensity:.4f},{stimulus_valence:.4f},{emotional_state.get_vector()},{action},{emotional_stability:.4f},{elapsed_time:.4f}\n")

#     #  12.  Вывод  результатов  в  консоль  (для  отладки)
#     print(f"Итерация:  {iteration}")
#     print(f"Интенсивность  стимула:  {stimulus_intensity:.4f},  Валентность:  {stimulus_valence:.4f}")
#     print(f"Вектор  эмоционального  состояния:  {emotional_state.get_vector()}")
#     print(f"Выбранное  действие:  {action}")
#     print(f"Эмоциональная  устойчивость:  {emotional_stability:.4f}")
#     print(f"Время  итерации:  {elapsed_time:.4f}\n")

# print(f"Результаты  сохранены  в  файл:  {filename}")

#  Открываем  файл  для  записи
with  open(filename,  'w')  as  f:
    #  Запись  заголовков  столбцов
    f.write("Iteration,Stimulus Intensity,Stimulus Valence,Joy,Sadness,Anger,Fear,Surprise,Disgust,Action,Emotional Stability,Time\n")  

    #  Запись  описания  действий
    f.write("Action description:  0 - Выразить  радость,  1 - Проявить  грусть,  2 - Проявить  гнев,  3 - Избегать  опасности,  4 - Взаимодействовать  с  объектом,  5 - Не  выражать  эмоций\n")  

    #  Генерация  обучающих  данных  для  EmotionalStabilityModel
    num_training_samples = 1000
    X_train,  y_train = emotional_stability_model.generate_training_data(num_training_samples)

    #  Разделяем  X_train  на  три  отдельных  массива
    history_train = X_train[:,  emotional_state.size:emotional_state.size  *  6]
    current_state_train = X_train[:,  :emotional_state.size]
    graph_weights_train = X_train[:,  emotional_state.size  *  6:]

    #  Преобразуем  данные  в  нужный  формат
    history_train = history_train.reshape((history_train.shape[0],  5,  emotional_state.size))
    current_state_train = current_state_train.reshape((current_state_train.shape[0],  emotional_state.size))
    graph_weights_train = graph_weights_train.reshape((graph_weights_train.shape[0],  6,  6))  

    #  Обучение  EmotionalStabilityModel
    emotional_stability_model.train([history_train,  current_state_train,  graph_weights_train],  y_train,  epochs=epochs,  batch_size=batch_size)  

    #  Пример  взаимодействия
    for  iteration  in  range(25):
        start_time = time.time()

        #  1.  Получение  стимула  (случайные  значения)
        stimulus_intensity = random.uniform(0,  1)
        stimulus_valence = random.uniform(-1,  1)

        #  2.  Установка  стимула
        stimulus_model.set_stimulus(stimulus_intensity,  stimulus_valence)

        #  3.  EmotionalModule  обрабатывает  стимул
        emotional_module.process_stimulus(stimulus_intensity,  stimulus_valence)

        #  4.  Обновление  EmotionGraph
        emotional_module.update_emotion_graph()

        #  5.  Обновление  истории  эмоциональных  состояний
        emotional_state.update_history()

        #  6.  Взаимодействие  с  TemperamentModel
        current_state = [0.5,  0.2,  1]  #  Пример  вектора  состояния
        action = temperament_model.get_action(current_state)

        #  7.  Определение  вознаграждения  (пример)
        reward = 0
        if  action == 0  and  emotional_state.get_emotion_intensity(0)  >  0.8:  #  Выразить  радость,  если  радость  высокая
            reward = 1
        elif  action == 3  and  emotional_state.get_emotion_intensity(3)  >  0.8:  #  Избегать  опасности,  если  страх  высокий
            reward = 1
        else:
            reward = -0.1  #  Небольшое  отрицательное  вознаграждение  за  другие  действия

        #  8.  Обновление  Q-таблицы
        next_state = [0.6,  0.1,  0.3]  #  Пример  следующего  состояния  (вам  нужно  определить  логику  перехода  между  состояниями)
        next_state = np.clip(next_state,  0,  1)
        temperament_model.update_q_table(current_state,  action,  reward,  next_state)

        #  9.  Взаимодействие  с  EmotionalStabilityModel  (только  если  есть  достаточно  данных)
        if len(emotional_state.get_history()) >= 5:
            current_emotional_state = emotional_state.get_vector()
            emotional_history = emotional_state.get_history()[-5:]  #  Последние  5  состояний
            emotion_graph_weights = emotion_graph.weights
            emotional_stability = emotional_stability_model.predict_emotional_stability(
                current_emotional_state,  emotional_history,  emotion_graph_weights
            )
        else:
            emotional_stability = 0.5  #  Значение  по  умолчанию,  если  история  слишком  короткая

        #  10.  Моделирование  изменения  эмоций  со  временем
        time_step = 0.1
        emotional_module.evolve(time_step)

        #  11.  Запись  результатов  в  файл
        end_time = time.time()
        elapsed_time = end_time - start_time
        f.write(f"{iteration},{stimulus_intensity:.4f},{stimulus_valence:.4f},{emotional_state.get_vector()},{action},{emotional_stability:.4f},{elapsed_time:.4f}\n")

        #  12.  Вывод  результатов  в  консоль  (для  отладки)
        print(f"Итерация:  {iteration}")
        print(f"Интенсивность  стимула:  {stimulus_intensity:.4f},  Валентность:  {stimulus_valence:.4f}")
        print(f"Вектор  эмоционального  состояния:  {emotional_state.get_vector()}")
        print(f"Выбранное  действие:  {action}")
        print(f"Эмоциональная  устойчивость:  {emotional_stability:.4f}")
        print(f"Время  итерации:  {elapsed_time:.4f}\n")

print(f"Результаты  сохранены  в  файл:  {filename}")