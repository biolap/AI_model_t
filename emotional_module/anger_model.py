from universal_system import UniversalSystem
import skfuzzy as fuzz
class AngerModel(UniversalSystem):
    def __init__(self, emotional_state):
        super().__init__("anger", emotional_state)
        #  Кварки  (примеры  значений)
        self.add_quark("threshold", 0.6)
        self.add_quark("intensity_factor", 1.5)
        self.add_quark("decay_rate", 0.05)
        #  Лептоны
        self.add_lepton("intensity", 0.0)

        #  Fuzzy  logic  компоненты  
        self.add_intensity_consequent("anger_intensity")
        # Call define_rules to initialize the simulation
        self.define_rules() 

    def define_rules(self):
        #  Добавьте  fuzzy-множество  'very_low'  для  self.intensity
        self.intensity['very_low'] = fuzz.trimf(self.intensity.universe, [0, 0, 0.25]) 

        super().add_rule("anger", self.stimulus_intensity['high'] & self.stimulus_valence['negative'], self.intensity['high'])
        super().add_rule("anger", self.stimulus_intensity['medium'] & self.stimulus_valence['negative'], self.intensity['medium'])
        super().add_rule("anger", self.stimulus_intensity['low'] & self.stimulus_valence['negative'], self.intensity['low'])
        super().add_rule("anger", self.stimulus_intensity['high'] & self.stimulus_valence['positive'], self.intensity['very_low'])
        super().add_rule("anger", self.stimulus_intensity['medium'] & self.stimulus_valence['positive'], self.intensity['very_low'])
        super().add_rule("anger", self.stimulus_intensity['low'] & self.stimulus_valence['positive'], self.intensity['very_low'])
        #  Создание  симуляции
        super().set_simulation("anger", self.rules["anger"])

    def interact(self, other_system):
        #  Электромагнитное  взаимодействие
        if other_system.name == "Stimulus":
            stimulus_valence = other_system.leptons["valence"]

            if stimulus_valence < 0:  #  Гнев  усиливается  только  при  отрицательной  валентности
                stimulus_intensity = other_system.leptons["intensity"]  #  Используется  косвенно  в  calculate_intensity
                self.leptons["intensity"] = self.calculate_intensity("anger", "anger_intensity", stimulus_intensity, stimulus_valence)  #  Добавлено
            else:
                self.leptons["intensity"] = 0.0

        #  Гравитационное  взаимодействие  (пример  с  "средой")
        if other_system.name == "Environment":
            if other_system.leptons["safety"] == "dangerous":
                self.leptons["intensity"] *= 1.2  #  Увеличиваем  интенсивность  в  опасной  среде
            elif other_system.leptons["stimulation"] == "high":
                self.leptons["intensity"] *= 0.8  #  Уменьшаем  интенсивность  в  стимулирующей  среде

    def evolve(self, time_step):
        #  Затухание  гнева
        self.leptons["intensity"] *= (1 - self.quarks["decay_rate"] * time_step)

        #  Убедимся,  что  интенсивность  не  станет  отрицательной
        self.leptons["intensity"] = max(self.leptons["intensity"], 0.0)