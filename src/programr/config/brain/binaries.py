from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData


class BrainBinariesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        super().__init__("binaries")
        self._save_binary = False
        self._load_binary = False
        self._binary_filename = None
        self._load_aiml_on_binary_fail = False

    @property
    def save_binary(self):
        return self._save_binary

    @property
    def load_binary(self):
        return self._load_binary

    @property
    def binary_filename(self):
        return self._binary_filename

    @property
    def load_aiml_on_binary_fail(self):
        return self._load_aiml_on_binary_fail

    def load_config_section(self, configuration_file, configuration, bot_root):
        binaries = configuration_file.get_section("binaries", configuration)
        if binaries is not None:
            self._save_binary = configuration_file.get_option(binaries, "save_binary", missing_value=None)
            self._load_binary = configuration_file.get_option(binaries, "load_binary", missing_value=None)
            binary_filename = configuration_file.get_option(binaries, "binary_filename", missing_value=None)
            if binary_filename is not None:
                self._binary_filename = self.sub_bot_root(binary_filename, bot_root)
            self._load_aiml_on_binary_fail = configuration_file.get_option(binaries, "load_aiml_on_binary_fail", missing_value=None)
        else:
            YLogger.warning(self, "'binaries' section missing from bot config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['save_binary'] = False
            data['load_binary'] = False
            data['binary_filename'] = "./braintree.bin"
            data['load_aiml_on_binary_fail'] = True
        else:
            data['save_binary'] = self._save_binary
            data['load_binary'] = self._load_binary
            data['binary_filename'] = self._binary_filename
            data['load_aiml_on_binary_fail'] = self._load_aiml_on_binary_fail
