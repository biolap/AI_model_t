# import networkx as nx
# class EmotionGraph:
#     def __init__(self):
#         self.graph = nx.DiGraph()
#         self.emotions = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
#         self.graph.add_nodes_from(self.emotions)
#         #  Пример матрицы весов (измените значения в соответствии с вашей моделью)
#         self.weights = [
#             [0.0, -0.5, -0.6, -0.7, 0.2, -0.4],  # joy
#             [-0.3, 0.0, 0.3, 0.6, 0.1, 0.2],  # sadness
#             [-0.4, 0.4, 0.0, 0.7, 0.0, 0.5],  # anger
#             [-0.5, 0.5, 0.6, 0.0, 0.1, 0.6],  # fear
#             [0.3, 0.2, 0.1, 0.0, 0.0, -0.3],  # surprise
#             [-0.2, 0.3, 0.4, 0.5, 0.0, 0.0],  # disgust
#         ]
#         # Добавление ребер с весами
#         for i, emotion1 in enumerate(self.emotions):
#             for j, emotion2 in enumerate(self.emotions):
#                 if i != j:  # Не добавляем ребра от эмоции к самой себе
#                     self.graph.add_edge(emotion1, emotion2, weight=self.weights[i][j])
#     def get_influence(self, emotion1, emotion2):
#         # Возвращает вес ребра от emotion1 к emotion2
#         return self.graph.get_edge_data(emotion1, emotion2)['weight']

import networkx as nx

class EmotionGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.emotions = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]
        self.graph.add_nodes_from(self.emotions)
        
        #  Матрица весов, отражающая влияние эмоций друг на друга
        self.weights = [
            [0.0, -0.6, -0.4, -0.5,  0.3, -0.3],  # joy
            [-0.3,  0.0,  0.4,  0.5, -0.2,  0.3],  # sadness
            [-0.2,  0.2,  0.0,  0.2, -0.3,  0.5],  # anger
            [-0.3,  0.3, -0.4,  0.0,  0.2,  0.6],  # fear
            [0.1, -0.1,  0.0, -0.2,  0.0, -0.4],  # surprise
            [-0.1,  0.2,  0.4,  0.5, -0.1,  0.0],  # disgust
        ]

        # Добавление ребер с весами
        for i, emotion1 in enumerate(self.emotions):
            for j, emotion2 in enumerate(self.emotions):
                if i != j:  # Не добавляем ребра от эмоции к самой себе
                    self.graph.add_edge(emotion1, emotion2, weight=self.weights[i][j])

    def get_influence(self, emotion1, emotion2):
        # Возвращает вес ребра от emotion1 к emotion2
        return self.graph.get_edge_data(emotion1, emotion2)['weight']