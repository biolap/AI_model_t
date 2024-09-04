from universal_system import UniversalSystem

class JoyModel(UniversalSystem):
    def __init__(self, emotional_state):
        super().__init__("joy", emotional_state)
        #  Кварки
        self.add_quark("threshold", 0.5)
        self.add_quark("intensity_factor", 1.2)
        self.add_quark("decay_rate", 0.1)
        #  Лептоны
        self.add_lepton("intensity", 0.0)

        #  Fuzzy  logic  компоненты  (уже  определены  в  UniversalSystem)
        self.add_intensity_consequent("joy_intensity")

        #  Правила
        super().add_rule("joy", self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['high'])  #  Исправлено
        super().add_rule("joy", self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['medium'])  #  Исправлено
        super().add_rule("joy", self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['low'])  #  Исправлено
        super().add_rule("joy", self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['low'])  #  Исправлено
        super().add_rule("joy", self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['low'])  #  Исправлено
        super().add_rule("joy", self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low'])  #  Исправлено

        #  Создание  симуляции
        super().set_simulation("joy", self.rules["joy"])  #  Исправлено
    def interact(self, other_system):
        #  Электромагнитное  взаимодействие
        if other_system.name == "Stimulus":
            stimulus_valence = other_system.leptons["valence"]
            #  Изменяем  интенсивность  радости  на  основе  стимула
            if stimulus_valence > 0:
                self.leptons["intensity"] = self.calculate_intensity("joy", "joy_intensity")
            else:
                self.leptons["intensity"] = 0.0
        #  Гравитационное  взаимодействие  (пример  с  "средой")
        if other_system.name == "Environment":
            if other_system.leptons["safety"] == "dangerous":
                self.leptons["intensity"] *= 0.5  #  Уменьшаем  интенсивность  в  опасной  среде
            elif other_system.leptons["stimulation"] == "high":
                self.leptons["intensity"] *= 1.2  #  Увеличиваем  интенсивность  в  стимулирующей  среде
    def evolve(self, time_step):
        #  Затухание  радости
        self.leptons["intensity"] *= (1 - self.quarks["decay_rate"] * time_step)

        #  Убедимся,  что  интенсивность  не  станет  отрицательной
        self.leptons["intensity"] = max(self.leptons["intensity"], 0.0)