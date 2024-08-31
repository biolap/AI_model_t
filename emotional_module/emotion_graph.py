import networkx as nx

class EmotionGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.emotions = ["joy", "sadness", "anger", "fear", "surprise"]
        self.graph.add_nodes_from(self.emotions)
        
        #  Пример матрицы весов (измените значения в соответствии с вашей моделью)
        self.weights = [
            [0.0, -0.5, -0.6, -0.7, 0.2],  # joy
            [-0.3, 0.0, 0.3, 0.6, 0.1],  # sadness
            [-0.4, 0.4, 0.0, 0.7, 0.0],  # anger
            [-0.5, 0.5, 0.6, 0.0, 0.1],  # fear
            [0.3, 0.2, 0.1, 0.0, 0.0],  # surprise
        ]
        
        # Добавление ребер с весами
        for i, emotion1 in enumerate(self.emotions):
            for j, emotion2 in enumerate(self.emotions):
                if i != j:  # Не добавляем ребра от эмоции к самой себе
                    self.graph.add_edge(emotion1, emotion2, weight=self.weights[i][j])

    def get_influence(self, emotion1, emotion2):
        # Возвращает вес ребра от emotion1 к emotion2
        return self.graph.get_edge_data(emotion1, emotion2)['weight']