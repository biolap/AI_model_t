from universal_system import UniversalSystem
import skfuzzy as fuzz
class FearModel(UniversalSystem):
    def __init__(self, emotional_state):
        super().__init__("fear", emotional_state)
        #  Кварки  (примеры  значений)
        self.add_quark("threshold", 0.7)
        self.add_quark("intensity_factor", 1.8)
        self.add_quark("decay_rate", 0.08)
        #  Лептоны
        self.add_lepton("intensity", 0.0)

        #  Fuzzy  logic  компоненты
        self.add_intensity_consequent("fear_intensity")
        # Call define_rules to initialize the simulation
        self.define_rules() 

        # #  Правила
        # super().add_rule("fear", self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['high'])
        # super().add_rule("fear", self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['medium'])
        # super().add_rule("fear", self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low'])
        # super().add_rule("fear", self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['low'])
        # super().add_rule("fear", self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['low'])
        # super().add_rule("fear", self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['low'])
    def define_rules(self):
        #  Добавьте  fuzzy-множество  'very_low'  для  self.intensity
        self.intensity['very_low'] = fuzz.trimf(self.intensity.universe, [0, 0, 0.25]) 

        super().add_rule("fear", self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['high'])
        super().add_rule("fear", self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['medium'])
        super().add_rule("fear", self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low'])
        super().add_rule("fear", self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['very_low'])
        super().add_rule("fear", self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['very_low'])
        super().add_rule("fear", self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['very_low'])
        #  Создание  симуляции
        super().set_simulation("fear", self.rules["fear"])

    def interact(self, other_system):
        #  Электромагнитное  взаимодействие
        if other_system.name == "Stimulus":
            stimulus_valence = other_system.leptons["valence"]

            #  Изменяем  интенсивность  страха  на  основе  стимула
            if stimulus_valence < 0:
                stimulus_intensity = other_system.leptons["intensity"]
                self.leptons["intensity"] = self.calculate_intensity("fear", "fear_intensity", stimulus_intensity, stimulus_valence)  #  Добавлено
            else:
                self.leptons["intensity"] = 0.0

        #  Гравитационное  взаимодействие  (пример  с  "средой")
        if other_system.name == "Environment":
            if other_system.leptons["safety"] == "dangerous":
                self.leptons["intensity"] *= 1.3  #  Увеличиваем  интенсивность  в  опасной  среде
            elif other_system.leptons["stimulation"] == "high":
                self.leptons["intensity"] *= 0.7  #  Уменьшаем  интенсивность  в  стимулирующей  среде

    def evolve(self, time_step):
        #  Затухание  страха
        self.leptons["intensity"] *= (1 - self.quarks["decay_rate"] * time_step)

        #  Убедимся,  что  интенсивность  не  станет  отрицательной
        self.leptons["intensity"] = max(self.leptons["intensity"], 0.0)