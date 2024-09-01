from fuzzylogic import FuzzyVariable, FuzzySet, FuzzyRule, FuzzySystem
from fuzzylogic.functions import TriangularMF


class EmotionalRangeModel:
    def __init__(self, emotional_state):
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
        self.sadness_intensity = FuzzyVariable(
            universe=(0, 1),
            terms={
                "Низкая": FuzzySet(function=TriangularMF(0, 0, 0.5)),
                "Средняя": FuzzySet(function=TriangularMF(0.25, 0.5, 0.75)),
                "Высокая": FuzzySet(function=TriangularMF(0.5, 1, 1)),
            },
        )
        self.anger_intensity = FuzzyVariable(
            universe=(0, 1),
            terms={
                "Низкая": FuzzySet(function=TriangularMF(0, 0, 0.5)),
                "Средняя": FuzzySet(function=TriangularMF(0.25, 0.5, 0.75)),
                "Высокая": FuzzySet(function=TriangularMF(0.5, 1, 1)),
            },
        )
        self.fear_intensity = FuzzyVariable(
            universe=(0, 1),
            terms={
                "Низкая": FuzzySet(function=TriangularMF(0, 0, 0.5)),
                "Средняя": FuzzySet(function=TriangularMF(0.25, 0.5, 0.75)),
                "Высокая": FuzzySet(function=TriangularMF(0.5, 1, 1)),
            },
        )
        self.surprise_intensity = FuzzyVariable(
            universe=(0, 1),
            terms={
                "Низкая": FuzzySet(function=TriangularMF(0, 0, 0.5)),
                "Средняя": FuzzySet(function=TriangularMF(0.25, 0.5, 0.75)),
                "Высокая": FuzzySet(function=TriangularMF(0.5, 1, 1)),
            },
        )

        # Определение правил fuzzy logic (для каждой эмоции)
        # --- Радость (Joy) ---
        self.rule1_joy = FuzzyRule(
            antecedent=(self.stimulus_intensity["Высокая"] & self.stimulus_valence["Положительная"]),
            consequent=self.joy_intensity["Высокая"],
        )
        self.rule2_joy = FuzzyRule(
            antecedent=(self.stimulus_intensity["Средняя"] & self.stimulus_valence["Положительная"]),
            consequent=self.joy_intensity["Средняя"],
        )
        self.rule3_joy = FuzzyRule(
            antecedent=(self.stimulus_intensity["Низкая"] & self.stimulus_valence["Положительная"]),
            consequent=self.joy_intensity["Низкая"],
        )

        # --- Грусть (Sadness) ---
        self.rule1_sadness = FuzzyRule(
            antecedent=(self.stimulus_intensity["Высокая"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.sadness_intensity["Высокая"],
        )
        self.rule2_sadness = FuzzyRule(
            antecedent=(self.stimulus_intensity["Средняя"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.sadness_intensity["Средняя"],
        )
        self.rule3_sadness = FuzzyRule(
            antecedent=(self.stimulus_intensity["Низкая"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.sadness_intensity["Низкая"],
        )

        # --- Гнев (Anger) ---
        self.rule1_anger = FuzzyRule(
            antecedent=(self.stimulus_intensity["Высокая"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.anger_intensity["Высокая"],
        )
        self.rule2_anger = FuzzyRule(
            antecedent=(self.stimulus_intensity["Средняя"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.anger_intensity["Средняя"],
        )
        self.rule3_anger = FuzzyRule(
            antecedent=(self.stimulus_intensity["Низкая"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.anger_intensity["Низкая"],
        )

        # --- Страх (Fear) ---
        self.rule1_fear = FuzzyRule(
            antecedent=(self.stimulus_intensity["Высокая"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.fear_intensity["Высокая"],
        )
        self.rule2_fear = FuzzyRule(
            antecedent=(self.stimulus_intensity["Средняя"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.fear_intensity["Средняя"],
        )
        self.rule3_fear = FuzzyRule(
            antecedent=(self.stimulus_intensity["Низкая"] & self.stimulus_valence["Отрицательная"]),
            consequent=self.fear_intensity["Низкая"],
        )

        # --- Удивление (Surprise) ---
        self.rule1_surprise = FuzzyRule(
            antecedent=(self.stimulus_intensity["Высокая"] & self.stimulus_valence["Нейтральная"]),
            consequent=self.surprise_intensity["Высокая"],
        )
        self.rule2_surprise = FuzzyRule(
            antecedent=(self.stimulus_intensity["Средняя"] & self.stimulus_valence["Нейтральная"]),
            consequent=self.surprise_intensity["Средняя"],
        )
        self.rule3_surprise = FuzzyRule(
            antecedent=(self.stimulus_intensity["Низкая"] & self.stimulus_valence["Нейтральная"]),
            consequent=self.surprise_intensity["Низкая"],
        )

        # Создание системы fuzzy logic
        self.fuzzy_system = FuzzySystem()

        # Добавление правил в систему
        self.fuzzy_system.add_rules(
            self.rule1_joy, self.rule2_joy, self.rule3_joy,
            self.rule1_sadness, self.rule2_sadness, self.rule3_sadness,
            self.rule1_anger, self.rule2_anger, self.rule3_anger,
            self.rule1_fear, self.rule2_fear, self.rule3_fear,
            self.rule1_surprise, self.rule2_surprise, self.rule3_surprise,
        )

        #  Сохранение  emotional_state  как атрибут класса
        self.emotional_state = emotional_state

    def get_emotion_intensity(self, emotion, stimulus_intensity, stimulus_valence):
        # Установка входных значений для системы fuzzy logic
        self.stimulus_intensity.value = stimulus_intensity
        self.stimulus_valence.value = stimulus_valence

        # Вычисление интенсивности эмоции
        self.fuzzy_system.calculate()

        # Обновление EmotionalState
        if emotion == "joy":
            self.emotional_state.set_emotion_intensity(0, self.joy_intensity.value)
        elif emotion == "sadness":
            self.emotional_state.set_emotion_intensity(1, self.sadness_intensity.value)
        elif emotion == "anger":
            self.emotional_state.set_emotion_intensity(2, self.anger_intensity.value)
        elif emotion == "fear":
            self.emotional_state.set_emotion_intensity(3, self.fear_intensity.value)
        elif emotion == "surprise":
            self.emotional_state.set_emotion_intensity(4, self.surprise_intensity.value)
        else:
            raise ValueError(f"Invalid emotion: {emotion}")

        # Возвращаем интенсивность 
        if emotion == "joy":
            return self.joy_intensity.value
        elif emotion == "sadness":
            return self.sadness_intensity.value
        elif emotion == "anger":
            return self.anger_intensity.value
        elif emotion == "fear":
            return self.fear_intensity.value
        elif emotion == "surprise":
            return self.surprise_intensity.value
        else:
            raise ValueError(f"Invalid emotion: {emotion}")