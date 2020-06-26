from programr.utils.logging.ylogger import YLogger

from programr.config.base import BaseConfigurationData


class BrainSemanticSimilarityConfiguration(BaseConfigurationData):

    def __init__(self):
        super().__init__(name="semantic_similarity")
        self._method = None

    @property
    def method(self):
        return self._method

    @property
    def model_dir(self):
        return self._model_dir

    # TODO: Add model_dir to load_config_section
    def load_config_section(self, configuration_file, configuration, bot_root):
        semantic_similarity = configuration_file.get_section(self._section_name, configuration)
        if semantic_similarity is not None:
            self._method = configuration_file.get_option(semantic_similarity, "method", missing_value="default")
        else:
            YLogger.warning(self, "'semantic_similarity' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['method'] = "embedding"
        else:
            data['method'] = self._method
