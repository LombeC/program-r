from programr.config.brain.nlp import BrainNLPConfiguration
from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration
from programr.config.brain.sentiment_analysis import BrainSentimentAnalysisConfiguration
from transformers import (RobertaTokenizer, RobertaForSequenceClassification, InputExample, TextClassificationPipeline,
                          glue_convert_examples_to_features, DistilBertTokenizer, DistilBertForSequenceClassification)
import torch
import numpy as np
from programr.utils.logging.ylogger import YLogger


class SentimentAnalysis():

    def __init__(self, ):
        pass

    # @staticmethod
    # def factory(config: BrainNLPConfiguration):
    #     if config.sentiment_analysis.method == "corenlp":
    #         print("corenlp is not supported anymore")
    #     elif config.sentiment_analysis.method == "distilbert":
    #         print("Using distilbert for sentiment analysis")
    #         return DistilBertSentimentAnalysis(config.sentiment_analysis)
    #     elif config.sentiment_analysis.method == "default":
    #         return DefaultSentimentAnalysis()

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
        # self._semantic_analysis_config = semantic_analysis_config
        # model_dir = semantic_analysis_config.model_dir
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



class SemanticSimilarity():

    def __init__(self):
        pass

    # @staticmethod
    # def factory(type_):
    #     if type_ == "embedding":
    #         return DistilRobertaSemanticSimilarity()

    #     elif type_ == "default":
    #         return DefaultSemanticSimilarity()

    #     else:
    #         YLogger.warning(DefaultSemanticSimilarity, "the module is unknown, defaulting to DefaultSemanticSimilarity")
    #         return DefaultSemanticSimilarity()

    def similarity_with_concepts(self, text, concepts):
        raise NotImplementedError("Should be override to be used.")

    def similarity_with_concept(self, text, concept):
        raise NotImplementedError("")


class DistilRobertaSemanticSimilarity(SemanticSimilarity):

    def __init__(self):
        super().__init__()
        # self.tokenizer = RobertaTokenizer.from_pretrained('./libs/pretrain_roberta_model')
        # self.model = RobertaForSequenceClassification.from_pretrained('./libs/pretrain_roberta_model')

        self.tokenizer = RobertaTokenizer.from_pretrained('./libs/pretrain_distilroberta')
        self.model = RobertaForSequenceClassification.from_pretrained('./libs/pretrain_distilroberta')

    def similarity_with_concept(self, text, concept):
        example = InputExample(guid='0', text_a=text, text_b=concept)
        feature = glue_convert_examples_to_features(examples=[example],
                                                    tokenizer=self.tokenizer,
                                                    max_length=128,
                                                    output_mode='regression',
                                                    label_list=[None])

        input_ids = torch.tensor(feature[0].input_ids).unsqueeze(0)
        attention_mask = torch.tensor(feature[0].attention_mask).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)

        return outputs[0].item()

    def similarity_with_concepts(self, text, concepts):
        examples = [InputExample(guid='0', text_a=text, text_b=concept) for concept in concepts]
        features = glue_convert_examples_to_features(examples=examples,
                                                     tokenizer=self.tokenizer,
                                                     max_length=128,
                                                     output_mode='regression',
                                                     label_list=[None])

        input_ids = torch.tensor([feature.input_ids for feature in features])
        attention_mask = torch.tensor([feature.attention_mask for feature in features])

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            outputs = outputs[0].T.tolist()[0]

        return outputs