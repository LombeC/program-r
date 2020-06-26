from programr.utils.logging.ylogger import YLogger
import os

from programr.config.section import BaseSectionConfigurationData


class BrainDefaultsConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        super().__init__("defaults")
        self._default_get = "unknown"
        self._default_property = "unknown"
        self._default_map = "unknown"
        self._learnf_path = self._default_os_learnf_path()

    @staticmethod
    def _default_os_learnf_path():
        if os.name == 'posix':
            return '/tmp/learnf'
        elif os.name == 'nt':
            return 'C:\\Windows\\Temp\\leanf'
        return "."

    @property
    def default_get(self):
        return self._default_get

    @property
    def default_property(self):
        return self._default_property

    @property
    def default_map(self):
        return self._default_map

    @property
    def learnf_path(self):
        return self._learnf_path

    def load_config_section(self, configuration_file, configuration, bot_root):
        binaries = configuration_file.get_section("defaults", configuration)
        if binaries is not None:
            self._default_get = configuration_file.get_option(binaries, "default-get", missing_value=None)
            self._default_property = configuration_file.get_option(binaries, "default-property", missing_value=None)
            self._default_map = configuration_file.get_option(binaries, "default-map", missing_value=None)
            learnf_path = configuration_file.get_option(binaries, "learnf-path", missing_value=None)
            if learnf_path is not None:
                self._learnf_path = self.sub_bot_root(learnf_path, bot_root)
        else:
            YLogger.warning(self, "'defaults' section missing from bot config, using default defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['default_get'] = "unknown"
            data['default_property'] = "unknown"
            data['default_map'] = "unknown"
            data['learnf_path'] = self._default_os_learnf_path()
        else:
            data['default_get'] = self._default_get
            data['default_property'] = self._default_property
            data['default_map'] = self._default_map
            data['learnf_path'] = self._learnf_path
