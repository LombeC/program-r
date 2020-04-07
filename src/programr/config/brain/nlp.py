from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration
from programr.config.brain.sentence_segmentation import BrainSentenceSegmentationConfiguration
from programr.config.brain.tokenizer import BrainTokenizerConfiguration
from programr.config.brain.sentiment_analysis import BrainSentimentAnalysisConfiguration
from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData
from programr.config.brain.corenlp import BrainCoreNLPConfiguration


class BrainNLPConfiguration(BaseSectionConfigurationData):
    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "nlp")
        self._classname = None
        self._nltk_data_dir = None
        self._corenlp = BrainCoreNLPConfiguration()
        self._toknizer = BrainTokenizerConfiguration()
        self._sentence_segmentation = BrainSentenceSegmentationConfiguration()
        #self._semantic_similarity = BrainSemanticSimilarityConfiguration()
        self._sentiment_analysis = BrainSentimentAnalysisConfiguration()

    @property
    def classname(self):
        return self._classname

    @property
    def nltk_data_dir(self):
        return self._nltk_data_dir

    @property
    def corenlp(self):
        return self._corenlp

    @property
    def tokenizer(self):
        return self._toknizer

    @property
    def sentence_segmentation(self):
        return self._sentence_segmentation

    @property
    def semantic_similarity(self):
        return self._semantic_similarity

    @property
    def sentiment_analysis(self):
        return self._sentiment_analysis


    def load_config_section(self, configuration_file, configuration, bot_root):
        nlp = configuration_file.get_section("nlp", configuration)
        if nlp is not None:
            self._classname = configuration_file.get_option(nlp, "classname")
            self._nltk_data_dir = configuration_file.get_option(nlp, "nltk_data_dir")
            corenlp = self._corenlp.load_config_section(configuration_file, nlp, bot_root)
            tokenizer = self._toknizer.load_config_section(configuration_file, nlp, bot_root)
            sentence_segmentation = self._sentence_segmentation.load_config_section(configuration_file, nlp, bot_root)
            semantic_similarity = self._semantic_similarity.load_config_section(configuration_file, nlp, bot_root)
            sentiment_analysis = self._sentiment_analysis.load_config_section(configuration_file, nlp, bot_root)
        else:
            YLogger.warning(self, "Config section [services] missing from Brain, no nlp loaded")


    def to_yaml(self, data, defaults=True):
        data['classname'] = self._classname