import  random
import  time
import  numpy  as  np
from  transliterate  import  translit

from  emotional_module.temperament_model  import  TemperamentModel
from  emotional_module.emotional_stability_model  import  EmotionalStabilityModel
from  emotional_module.emotional_state  import  EmotionalState
from  emotional_module.stimulus_model  import  StimulusModel
from  emotional_module.environment_model  import  EnvironmentModel
from  emotional_module.emotional_module  import  EmotionalModule
from  emotional_module.emotion_graph  import  EmotionGraph
from  emotional_module.reward_system  import  calculate_reward

def  run_experiment(experiment_name,  lstm_units,  epochs,  batch_size,  num_iterations):
    """  Запускает  эксперимент  и  сохраняет  результаты  в  файл.  """

    #  Создание  файла  результатов
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"temp/results_{experiment_name}_{timestamp}.txt"

    #  Создание  экземпляров
    emotional_state = EmotionalState()
    emotion_graph = EmotionGraph()
    temperament_model = TemperamentModel(state_size,  action_size,  learning_rate,  discount_factor,  epsilon,  emotional_state,  emotion_graph)
    emotional_stability_model = EmotionalStabilityModel(input_shape=(5,  6),  emotion_graph=emotion_graph,  emotional_state=emotional_state,  lstm_units=lstm_units)
    stimulus_model = StimulusModel()
    environment_model = EnvironmentModel()
    emotional_module = EmotionalModule(emotional_state)

    #  Открываем  файл  для  записи
    with  open(filename,  'w')  as  f:
        #  Запись  заголовков  столбцов
        f.write("Iteration,Stimulus Intensity,Stimulus Valence,joy,sadness,anger,fear,surprise,disgust,Action,Emotional Stability,Time\n")

        # #  Запись  описания  действий
        # f.write(translit(
        #     "Описание  действий:  0  -  Выразить  радость,  1  -  Проявить  грусть,  2  -  Проявить  гнев,  3  -  Избегать  опасности,  4  -  Взаимодействовать  с  объектом,  5  -  Не  выражать  эмоций",
        #     'ru',  reversed=True
        # )  +  "\n")

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
        for  iteration  in  range(num_iterations):
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

            #  7.  Определение  вознаграждения
            reward = calculate_reward(action,  emotional_state,  emotion_graph)

            #  8.  Обновление  Q-таблицы
            next_state = [0.6,  0.1,  0.3]
            next_state = np.clip(next_state,  0,  1)
            temperament_model.update_q_table(current_state,  action,  reward,  next_state)

            #  9.  Взаимодействие  с  EmotionalStabilityModel
            if  len(emotional_state.get_history())  >=  5:
                current_emotional_state = emotional_state.get_vector()
                emotional_history = emotional_state.get_history()[-5:]
                emotion_graph_weights = emotion_graph.weights
                emotional_stability = emotional_stability_model.predict_emotional_stability(
                    current_emotional_state,  emotional_history,  emotion_graph_weights
                )
            else:
                emotional_stability = 0.5

            #  10.  Моделирование  изменения  эмоций  со  временем
            time_step = 0.1
            emotional_module.evolve(time_step)

            #  11.  Запись  результатов  в  файл
            end_time = time.time()
            elapsed_time = end_time - start_time
            emotional_state_vector = emotional_state.get_vector()
            f.write(f"{iteration},{stimulus_intensity:.4f},{stimulus_valence:.4f},"
                    f"{emotional_state_vector[0]:.4f},{emotional_state_vector[1]:.4f},{emotional_state_vector[2]:.4f},"
                    f"{emotional_state_vector[3]:.4f},{emotional_state_vector[4]:.4f},{emotional_state_vector[5]:.4f},"
                    f"{action},{emotional_stability:.4f},{elapsed_time:.4f}\n")

            #  12.  Вывод  результатов  в  консоль
            print(f"Iteration:  {iteration}")
            print(f"Stimulus  Intensity:  {stimulus_intensity:.4f},  Valence:  {stimulus_valence:.4f}")
            print(f"Emotional  State  Vector:  {emotional_state.get_vector()}")
            print(f"Selected  Action:  {action}")
            print(f"Emotional  Stability:  {emotional_stability:.4f}")
            print(f"Iteration  Time:  {elapsed_time:.4f}\n")

    print(f"The  results  are  saved  to  a  file:  {filename}")

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
num_iterations = 25  #  Количество  итераций  в  эксперименте

#  Запуск  эксперимента
run_experiment(experiment_name,  lstm_units,  epochs,  batch_size,  num_iterations)