from programr.utils.logging.ylogger import YLogger

from programr.config.base import BaseConfigurationData


class BrainSentimentAnalysisConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="sentiment_analysis")
        self._method = None
        self._alpha = None
        self._negative_threshold = None
        self._positive_thresehold = None


    @property
    def method(self):
        return self._method

    @property
    def positive_threshold(self):
        return self._positive_thresehold

    @property
    def negative_threshold(self):
        return self._negative_threshold

    @property
    def alpha(self):
        return self._alpha

    @property
    def model_dir(self):
        return self._model_dir

    def load_config_section(self, configuration_file, configuration, bot_root):
        sentiment_analysis = configuration_file.get_section(self._section_name, configuration)
        if sentiment_analysis is not None:
            self._method = configuration_file.get_option(sentiment_analysis, "method", missing_value="default")
            self._negative_threshold = configuration_file.get_float_option(sentiment_analysis, "negative_threshold", missing_value=0.1)
            self._positive_thresehold = configuration_file.get_float_option(sentiment_analysis, "positive_threshold", missing_value=-0.1)
            self._alpha = configuration_file.get_float_option(sentiment_analysis, "alpha", missing_value=0.0)
            self._model_dir = configuration_file.get_option(sentiment_analysis, "model_dir", missing_value="")
        else:
            YLogger.warning(self, "'sentiment_analysis' section missing from bot config, using defaults")


    def to_yaml(self, data, defaults=True):
        if defaults:
            data['method'] = "corenlp"
            data['positive_threshold'] = 0.2
            data['negative_threshold'] = -0.2
            data['alpha'] = 0.1
        else:
            data['method'] = self._method
            data['positive_threshold'] = self._positive_thresehold
            data['negative_threshold'] = self._negative_threshold
            data['alpha'] = self._alpha
