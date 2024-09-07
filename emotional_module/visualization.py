# # import plotly.graph_objects as go
# import networkx as nx
# import matplotlib.pyplot as plt


# # def visualize_emotion_graph_3d(emotion_graph, emotional_state):
# #     """Визуализирует граф эмоций в 3D.

# #     Args:
# #         emotion_graph: Экземпляр класса EmotionGraph.
# #         emotional_state: Экземпляр класса EmotionalState.
# #     """
# #     # Получаем интенсивность эмоций из emotional_state
# #     emotion_intensities = {
# #         emotion: emotional_state.get_emotion_intensity(i) 
# #         for i, emotion in enumerate(emotion_graph.emotions)
# #     }

# #     # Создаем макет графа в 3D
# #     pos = nx.spring_layout(emotion_graph.graph, dim=3)

# #     # Создаем списки координат узлов
# #     Xn = [pos[emotion][0] for emotion in emotion_graph.emotions]
# #     Yn = [pos[emotion][1] for emotion in emotion_graph.emotions]
# #     Zn = [pos[emotion][2] for emotion in emotion_graph.emotions]

# #     # Создаем след (trace) для узлов
# #     node_trace = go.Scatter3d(
# #         x=Xn,
# #         y=Yn,
# #         z=Zn,
# #         mode='markers',
# #         marker=dict(
# #             size=[intensity * 10 for intensity in emotion_intensities.values()],
# #             color=["lightblue" for _ in emotion_intensities.values()],  # Цвет узлов
# #         ),
# #         text=emotion_graph.emotions,  # Метки узлов
# #         hoverinfo='text'
# #     )

# #     #  Создаем  следы  (traces)  для  ребер
# #     edge_traces = []
# #     for edge in emotion_graph.graph.edges(data=True):
# #         x0, y0, z0 = pos[edge[0]]
# #         x1, y1, z1 = pos[edge[1]]

# #         #  Преобразуем  вес  в  неотрицательное  значение
# #         width = abs(edge[2]['weight']) * 2  #  Используем  abs()  для  получения  абсолютного  значения

# #         edge_trace = go.Scatter3d(
# #             x=[x0, x1, None],
# #             y=[y0, y1, None],
# #             z=[z0, z1, None],
# #             mode='lines',
# #             line=dict(
# #                 width=width,  #  Используем  преобразованное  значение  width
# #                 color="gray"
# #             ),
# #             hoverinfo='none'
# #         )
# #         edge_traces.append(edge_trace)

# #     # Создаем фигуру (figure) и добавляем следы
# #     fig = go.Figure(data=edge_traces + [node_trace])  # Добавляем все следы ребер и след узлов

# #     # Настройка макета фигуры
# #     fig.update_layout(
# #         title="Граф эмоций (3D)",
# #         showlegend=False,
# #         scene=dict(
# #             xaxis=dict(showticklabels=False, title=""),
# #             yaxis=dict(showticklabels=False, title=""),
# #             zaxis=dict(showticklabels=False, title="")
# #         ),
# #         margin=dict(l=0, r=0, b=0, t=40)
# #     )

# #     # Отображаем график
# #     fig.show()
    
# def visualize_emotion_graph(emotion_graph, emotional_state):
#     """Визуализирует граф эмоций.

#     Args:
#         emotion_graph: Экземпляр класса EmotionGraph.
#         emotional_state: Экземпляр класса EmotionalState.
#     """
#     # Получаем интенсивность эмоций из emotional_state
#     emotion_intensities = {
#         emotion: emotional_state.get_emotion_intensity(i) 
#         for i, emotion in enumerate(emotion_graph.emotions)
#     }

#     # Создаем макет графа
#     pos = nx.spring_layout(emotion_graph.graph)

#     # Рисуем узлы с размером,  пропорциональным интенсивности эмоции
#     node_sizes = [intensity * 1000 for intensity in emotion_intensities.values()]
#     nx.draw_networkx_nodes(emotion_graph.graph, pos, node_size=node_sizes, node_color="lightblue")

#     # Рисуем ребра с толщиной,  пропорциональной весу
#     edge_widths = [data['weight'] * 5 for _, _, data in emotion_graph.graph.edges(data=True)]
#     nx.draw_networkx_edges(emotion_graph.graph, pos, width=edge_widths, edge_color="gray")

#     # Добавляем метки к узлам
#     nx.draw_networkx_labels(emotion_graph.graph, pos, font_size=10)

#     # Отображаем граф
#     plt.title("Граф эмоций")
#     plt.axis('off')
#     plt.show()

# import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt

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
