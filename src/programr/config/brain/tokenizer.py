from programr.utils.logging.ylogger import YLogger

from programr.config.base import BaseConfigurationData


class BrainTokenizerConfiguration(BaseConfigurationData):

    def __init__(self):
        super().__init__(name="tokenizer")
        self._libname = None
        self._split_chars = " "

    @property
    def libname(self):
        return self._libname

    @property
    def split_chars(self):
        return self._split_chars

    def load_config_section(self, configuration_file, configuration, bot_root):
        tokenizer = configuration_file.get_section(self._section_name, configuration)
        if tokenizer is not None:
            self._libname = configuration_file.get_option(tokenizer, "libname", missing_value="default")
            self._split_chars = configuration_file.get_option(tokenizer, "split_chars", missing_value=" ")
        else:
            YLogger.warning(self, "'tokenizer' section missing from bot config, using defaults")


    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = "spacy"
            data['split_chars'] = ' '
        else:
            data['classname'] = self._libname
            data['split_chars'] = self._split_chars
