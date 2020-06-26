from programr.utils.logging.ylogger import YLogger

from programr.config.base import BaseConfigurationData


class BrainSentenceSegmentationConfiguration(BaseConfigurationData):

    def __init__(self):
        super().__init__(name="sentence_segmentation")
        self._libname = None

    @property
    def libname(self):
        return self._libname


    def load_config_section(self, configuration_file, configuration, bot_root):
        sentence_segmentation = configuration_file.get_section(self._section_name, configuration)
        if sentence_segmentation is not None:
            self._libname = configuration_file.get_option(sentence_segmentation, "libname", missing_value="default")
        else:
            YLogger.warning(self, "'sentence_segmentation' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['libname'] = "spacy"
        else:
            data['libname'] = self._libname
