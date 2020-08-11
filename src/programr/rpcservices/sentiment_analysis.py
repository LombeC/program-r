from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
import numpy as np
from programr.utils.logging.ylogger import YLogger


class SentimentAnalysis():

    def __init__(self, ):
        pass

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

    def __init__(self):
        super().__init__()
        tokenizer = DistilBertTokenizer.from_pretrained('./libs/pretrain_distilbert_full_sentiment')
        model = DistilBertForSequenceClassification.from_pretrained('./libs/pretrain_distilbert_full_sentiment')
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