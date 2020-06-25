from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData


class BrainOverridesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        super().__init__("overrides")
        self._allow_system_aiml = False
        self._allow_learn_aiml = False
        self._allow_learnf_aiml = False

    @property
    def allow_system_aiml(self):
        return self._allow_system_aiml

    @property
    def allow_learn_aiml(self):
        return self._allow_learn_aiml

    @property
    def allow_learnf_aiml(self):
        return self._allow_learnf_aiml

    def load_config_section(self, configuration_file, configuration, bot_root):
        overrides = configuration_file.get_section(self._section_name, configuration)
        if overrides is not None:
            self._allow_system_aiml = configuration_file.get_bool_option(overrides, "allow_system_aiml", missing_value=False)
            self._allow_learn_aiml = configuration_file.get_bool_option(overrides, "allow_learn_aiml", missing_value=False)
            self._allow_learnf_aiml = configuration_file.get_bool_option(overrides, "allow_learnf_aiml", missing_value=False)
        else:
            YLogger.warning(self, "'overrides' section missing from brain config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['allow_system_aiml'] = False
            data['allow_learn_aiml'] = False
            data['allow_learnf_aiml'] = False
        else:
            data['allow_system_aiml'] = self._allow_system_aiml
            data['allow_learn_aiml'] = self._allow_learn_aiml
            data['allow_learnf_aiml'] = self._allow_learnf_aiml
