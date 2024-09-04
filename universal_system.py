import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class UniversalSystem:
    def __init__(self, name, emotional_state=None):
        self.name = name
        self.emotional_state = emotional_state
        self.quarks = {}
        self.leptons = {}
        self.bosons = {
            "strong": None,
            "weak": None,
            "electromagnetic": None,
            "gravitational": None
        }
        self.fields = {}
        self.dark_matter = {}
        self.dark_energy = {}
        self.rules = {}
        self.simulations = {}

        #  Fuzzy  logic  компоненты
        self.stimulus_intensity = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'stimulus_intensity')
        self.stimulus_valence = ctrl.Antecedent(np.arange(-1, 1.1, 0.1), 'stimulus_valence')

        #  Определение  fuzzy-множеств
        for var in [self.stimulus_intensity, self.stimulus_valence]:
            var['low'] = fuzz.trimf(var.universe, [0, 0, 0.5])
            var['medium'] = fuzz.trimf(var.universe, [0.25, 0.5, 0.75])
            var['high'] = fuzz.trimf(var.universe, [0.5, 1, 1])

        self.stimulus_valence['negative'] = fuzz.trimf(self.stimulus_valence.universe, [-1, -1, 0])
        self.stimulus_valence['neutral'] = fuzz.trimf(self.stimulus_valence.universe, [-0.5, 0, 0.5])
        self.stimulus_valence['positive'] = fuzz.trimf(self.stimulus_valence.universe, [0, 1, 1])
        
    def add_intensity_consequent(self, intensity_name):
        """  Добавляет  fuzzy-переменную  для  интенсивности.  """
        self.intensity = ctrl.Consequent(np.arange(0, 1.1, 0.1), intensity_name)
        self.intensity['low'] = fuzz.trimf(self.intensity.universe, [0, 0, 0.5])
        self.intensity['medium'] = fuzz.trimf(self.intensity.universe, [0.25, 0.5, 0.75])
        self.intensity['high'] = fuzz.trimf(self.intensity.universe, [0.5, 1, 1])
    def add_quark(self, name, value):
        self.quarks[name] = value

    def add_lepton(self, name, value):
        self.leptons[name] = value

    def set_boson(self, interaction_type, value):
        if interaction_type in self.bosons:
            self.bosons[interaction_type] = value
        else:
            raise ValueError(f"Invalid interaction type: {interaction_type}")

    def add_field(self, name, value):
        self.fields[name] = value

    def add_dark_matter(self, name, value):
        self.dark_matter[name] = value

    def add_dark_energy(self, name, value):
        self.dark_energy[name] = value
        
    def add_rule(self, rule_set_name, antecedent, consequent):
        """  Добавляет  правило  fuzzy  logic  в  указанный  набор  правил.  

        Args:
            rule_set_name:  Имя  набора  правил,  в  который  нужно  добавить  правило.
            antecedent:  Антецедент  (часть  IF)  правила.
            consequent:  Консеквент  (часть  THEN)  правила.
        """
        if rule_set_name not in self.rules:
            self.rules[rule_set_name] = []
        self.rules[rule_set_name].append(ctrl.Rule(antecedent, consequent))

    def set_simulation(self, simulation_name, rules):
        """  Создает  и  сохраняет  симуляцию  fuzzy  logic.  

        Args:
            simulation_name:  Имя  симуляции.
            rules:  Список  правил  fuzzy  logic.
        """
        self.simulations[simulation_name] = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

    def interact(self, other_system):
        #  Логика  взаимодействия  с  другими  системами
        #  Здесь  вы  будете  определять,  как  эта  система  влияет  на  другие  системы
        #  и  как  другие  системы  влияют  на  эту  систему.
        pass

    def evolve(self, time_step):
        #  Логика  эволюции  системы  во  времени
        #  Здесь  вы  будете  определять,  как  состояние  системы  меняется  со  временем.
        pass