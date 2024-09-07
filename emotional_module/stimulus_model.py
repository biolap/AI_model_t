# from universal_system import UniversalSystem

# class StimulusModel(UniversalSystem):
#     def __init__(self):
#         super().__init__("Stimulus")
#         self.add_lepton("intensity", 0.0)
#         self.add_lepton("valence", 0.0)

#     def set_stimulus(self, intensity, valence):
#         """ Устанавливает параметры стимула.

#         Args:
#             intensity: Интенсивность стимула (от 0 до 1).
#             valence: Валентность стимула (от -1 до 1).
#         """
#         self.leptons["intensity"] = intensity
#         self.leptons["valence"] = valence

from universal_system import UniversalSystem

class StimulusModel(UniversalSystem):
    def __init__(self):
        super().__init__("Stimulus")
        self.add_lepton("intensity", 0.0)
        self.add_lepton("valence", 0.0)

    def set_stimulus(self, intensity, valence):
        """ Устанавливает параметры стимула.

        Args:
            intensity: Интенсивность стимула (от 0 до 1).
            valence: Валентность стимула (от -1 до 1).
        """
        self.leptons["intensity"] = intensity
        self.leptons["valence"] = valence