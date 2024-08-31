from fuzzylogic import *

class EmotionalRangeModel:
    def __init__(self):
        # Определение лингвистических переменных для интенсивности стимула
        self.stimulus_intensity = FuzzyVariable(
            universe=(0, 1),
            terms={
                "Низкая": FuzzySet(function=TriangularMF(0, 0, 0.5)),
                "Средняя": FuzzySet(function=TriangularMF(0.25, 0.5, 0.75)),
                "Высокая": FuzzySet(function=TriangularMF(0.5, 1, 1)),
            },
        )

        # Определение лингвистических переменных для валентности стимула
        self.stimulus_valence = FuzzyVariable(
            universe=(-1, 1),
            terms={
                "Отрицательная": FuzzySet(function=TriangularMF(-1, -1, 0)),
                "Нейтральная": FuzzySet(function=TriangularMF(-0.5, 0, 0.5)),
                "Положительная": FuzzySet(function=TriangularMF(0, 1, 1)),
            },
        )

        # Определение лингвистических переменных для интенсивности эмоций (для каждой эмоции)
        self.joy_intensity = FuzzyVariable(
            universe=(0, 1),
            terms={
                "Низкая": FuzzySet(function=TriangularMF(0, 0, 0.5)),
                "Средняя": FuzzySet(function=TriangularMF(0.25, 0.5, 0.75)),
                "Высокая": FuzzySet(function=TriangularMF(0.5, 1, 1)),
            },
        )
        # ... (повторите для других эмоций: sadness, anger, fear, surprise)

        # Определение правил fuzzy logic (для каждой эмоции)
        self.rule1_joy = FuzzyRule(
            antecedent=(self.stimulus_intensity["Высокая"] & self.stimulus_valence["Положительная"]),
            consequent=self.joy_intensity["Высокая"],
        )
        # ... (добавьте другие правила для радости)

        # ... (повторите для других эмоций: sadness, anger, fear, surprise)

        # Создание системы fuzzy logic
        self.fuzzy_system = FuzzySystem()
        # ... (добавьте все правила в систему)

    # ... (остальной код будет добавлен позже)
    