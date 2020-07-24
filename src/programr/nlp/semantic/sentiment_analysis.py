from programr.config.brain.nlp import BrainNLPConfiguration
from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration
from programr.config.brain.sentiment_analysis import BrainSentimentAnalysisConfiguration
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, TextClassificationPipeline
import torch
import numpy as np
from programr.utils.logging.ylogger import YLogger


class SentimentAnalysis():

    def __init__(self, ):
        pass

    @staticmethod
    def factory(config: BrainNLPConfiguration):
        if config.sentiment_analysis.method == "corenlp":
            print("corenlp is not supported anymore")
        elif config.sentiment_analysis.method == "distilbert":
            print("Using distilbert for sentiment analysis")
            return DistilBertSentimentAnalysis(config.sentiment_analysis)
        elif config.sentiment_analysis.method == "default":
            return DefaultSentimentAnalysis()

    def get_sentence_sentiment(self, sentence):
        raise NotImplementedError("Should be override to be used.")

    def get_sentences_sentiments(self, sentences):
        raise NotImplementedError("Should be override to be used.")

    def alpha(self):
        raise NotImplementedError("Should be override to be used.")

    def positive_threshold(self):
        raise NotImplementedError("Should be override to be used.")

    def negative_threshold(self):
        raise NotImplementedError("Should be override to be used.")


class SentimentClassifer:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def __call__(self, text):
        input_ids = torch.tensor(self.tokenizer.encode(text, add_special_tokens=True)).unsqueeze(0)
        outputs = self.model(input_ids)
        outputs = outputs[0].detach().numpy()
        scores = np.exp(outputs) / np.exp(outputs).sum(-1)
        scores = scores[0].tolist()
        result = {"negative": scores[0], "neutral": scores[1], "positive": scores[2]}
        return result


class DistilBertSentimentAnalysis(SentimentAnalysis):

    def __init__(self, semantic_analysis_config: BrainSentimentAnalysisConfiguration):
        super().__init__()
        self._semantic_analysis_config = semantic_analysis_config
        model_dir = semantic_analysis_config.model_dir
        tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
        model = DistilBertForSequenceClassification.from_pretrained(model_dir)
        self.sentiment_classifier = SentimentClassifer(model, tokenizer)

    def get_sentence_sentiment(self, sentence):
        result = self.sentiment_classifier(sentence)
        sentiment = max(result, key=result.get)
        sentiment_distribution = list(result.values())
        return sentiment, sentiment_distribution

    def get_sentences_sentiments(self, sentences):
        sentiments, sentiment_distributions = [], []
        for sentence in sentences:
            sentiment, sentiment_distribution = self.get_sentence_sentiment(sentence)
            sentiments.append(sentiment)
            sentiment_distributions.append(sentiment_distribution)

        return sentiments, sentiment_distributions

    def expected_sentiment_value(self, sentiment_distribution):
        value = -sentiment_distribution[0] + sentiment_distribution[2]
        return value

    @property
    def alpha(self):
        return self._semantic_analysis_config.alpha

    @property
    def positive_threshold(self):
        return self._semantic_analysis_config.positive_threshold

    @property
    def negative_threshold(self):
        return self._semantic_analysis_config.negative_threshold


class DefaultSentimentAnalysis(SentimentAnalysis):

    def __init__(self):
        super().__init__()

    def get_sentence_sentiment(self, sentence):
        return

    def get_sentences_sentiments(self, sentences):
        return

    def alpha(self):
        return

    def positive_threshold(self):
        return

    def negative_threshold(self):
        return


if __name__ == "__main__":
    semantic_analysis_config = BrainSentimentAnalysisConfiguration()
    semantic_analysis_config._model_dir = "/home/rohola/codes/program-r/libs/pretrain_distillbert_full_sst"
    s = DistilBertSentimentAnalysis(semantic_analysis_config)
    a = s.get_sentence_sentiment("this is so cute!")
    print(a)
    l = s.get_sentences_sentiments(["this is cute!", "that's horrible"])
    print(l)
    k = s.expected_sentiment_value(a[1])
    print(k)