from universal_system import UniversalSystem

class EnvironmentModel(UniversalSystem):
    def __init__(self):
        super().__init__("Environment")
        self.add_lepton("safety", "safe")  # По умолчанию среда безопасна
        self.add_lepton("stimulation", "medium")  # По умолчанию уровень стимуляции средний

    def set_safety(self, safety_level):
        """ Устанавливает уровень безопасности среды.

        Args:
            safety_level: Уровень безопасности ("safe", "dangerous").
        """
        self.leptons["safety"] = safety_level

    def set_stimulation(self, stimulation_level):
        """ Устанавливает уровень стимуляции среды.

        Args:
            stimulation_level: Уровень стимуляции ("low", "medium", "high").
        """
        self.leptons["stimulation"] = stimulation_level