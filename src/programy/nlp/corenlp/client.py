from pycorenlp import StanfordCoreNLP

from programy.config.brain.corenlp import BrainCoreNLPConfiguration
from programy.nlp.corenlp.server import StanfordCoreNLPServer


class Client():

    def __init__(self, configuration: BrainCoreNLPConfiguration):
        '''
        As you make an instance of the client the server starts to run
        '''
        corenlp_server = StanfordCoreNLPServer(corenlp_dir=configuration.jar_dir, port=configuration.port)
        corenlp_server.run()

        self._url = str(configuration.ip) + ":" + str(configuration.port)

    def get_sentence_sentiment(self, sentence):
        try:

            stanford_corenlp = StanfordCoreNLP(self._url)
            result = stanford_corenlp.annotate(sentence,
                                               properties={
                                   'annotators': 'sentiment',
                                   'outputFormat': 'json',
                                   'timeout': 5000,
                               })
        except:
            return None


        return result["sentences"][0]["sentiment"], result["sentences"][0]["sentimentValue"]


    def get_sentences_sentiments(self, sentences):
        try:

            stanford_corenlp = StanfordCoreNLP(self._url)
            result = stanford_corenlp.annotate(sentences,
                                               properties={
                                   'annotators': 'sentiment',
                                   'outputFormat': 'json',
                                   'timeout': 5000,
                               })
        except:
            return None

        sentiments = [sentiment_info["sentiment"] for sentiment_info in result["sentences"]]
        sentiment_values = [sentiment_info["sentimentValue"] for sentiment_info in result["sentences"]]
        return sentiments, sentiment_values


