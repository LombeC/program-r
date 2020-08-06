import numpy as np
import torch
import requests
import json

from programr.utils.logging.ylogger import YLogger
from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration
from transformers import (RobertaTokenizer, RobertaForSequenceClassification, InputExample,
                          glue_convert_examples_to_features)


class SemanticSimilarity():

    def __init__(self):
        pass

    @staticmethod
    def factory(type_):
        if type_ == "embedding":
            return DistilRobertaSemanticSimilarity()

        elif type_ == "default":
            return DefaultSemanticSimilarity()

        else:
            YLogger.warning(DefaultSemanticSimilarity, "the module is unknown, defaulting to DefaultSemanticSimilarity")
            return DefaultSemanticSimilarity()

    def similarity_with_concepts(self, text, concepts):
        raise NotImplementedError("Should be override to be used.")

    def similarity_with_concept(self, text, concept):
        raise NotImplementedError("")


class DistilRobertaSemanticSimilarity(SemanticSimilarity):

    def __init__(self, semantic_similarity_config: BrainSemanticSimilarityConfiguration):
        super().__init__()
        self.semantic_similarity_config = semantic_similarity_config
        model_dir = semantic_similarity_config.model_dir
        self.tokenizer = RobertaTokenizer.from_pretrained(model_dir)
        self.model = RobertaForSequenceClassification.from_pretrained(model_dir)

    def similarity_with_concept(self, text, concept):
        example = InputExample(guid='0', text_a=text, text_b=concept)
        feature = glue_convert_examples_to_features(examples=[example],
                                                    tokenizer=tokenizer,
                                                    max_length=128,
                                                    output_mode='regression',
                                                    label_list=[None])

        input_ids = torch.tensor(feature[0].input_ids).unsqueeze(0)
        attention_mask = torch.tensor(feature[0].attention_mask).unsqueeze(0)

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)

        return outputs[0].item()

    def similarity_with_concepts(self, text, concepts):
        examples = [InputExample(guid='0', text_a=text, text_b=concept) for concept in concepts]
        features = glue_convert_examples_to_features(examples=examples,
                                                     tokenizer=tokenizer,
                                                     max_length=128,
                                                     output_mode='regression',
                                                     label_list=[None])

        input_ids = torch.tensor([feature.input_ids for feature in features])
        attention_mask = torch.tensor([feature.attention_mask for feature in features])

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            outputs = outputs[0].T.tolist()[0]

        return outputs


class DefaultSemanticSimilarity(SemanticSimilarity):

    def __init__(self):
        pass

    def similarity_with_concept(self, text, concept):
        pass

    def similarity_with_concepts(self, text, concepts):
        pass


if __name__ == "__main__":
    tokenizer = RobertaTokenizer.from_pretrained('./libs/pretrain_roberta_model')
    model = RobertaForSequenceClassification.from_pretrained('./libs/pretrain_roberta_model')

    sentence1 = "Dogs are cute."
    sentence2 = "I need an Macbook."
    sentence3 = "Computer technology is awesome."

    example = InputExample(guid=0, text_a=sentence3, text_b=sentence2, label=0)
    feature = glue_convert_examples_to_features(examples=[example],
                                                tokenizer=tokenizer,
                                                max_length=128,
                                                output_mode='regression',
                                                label_list=[None])

    input_ids = torch.tensor(feature[0].input_ids).unsqueeze(0)
    attention_mask = torch.tensor(feature[0].attention_mask).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        print("model outputs: {}".format(outputs[0].item()))

    config = BrainSemanticSimilarityConfiguration()
    config._model_dir = "./libs/pretrain_roberta_model"
    semantic_similarity = DistilRobertaSemanticSimilarity(config)
    s1 = semantic_similarity.similarity_with_concept("The computer technology is awesome", "Intel")
    s2 = semantic_similarity.similarity_with_concept("The computer technology is awesome", "dog")
    print("semantics similarity scores: {}, {}".format(s1, s2))

    ss = semantic_similarity.similarity_with_concepts("The computer technology is awesome",
                                                      ["dogs", "peperoni", "Intel"])
    print("semantics similarity scores: {}".format(ss))

    # NOTE: Tensorflow version
    # semantic_similarity = EmbeddingSemanticSimilarity()
    # result = semantic_similarity.similarity_with_concept("Hi", "greeting")
    # result1 = semantic_similarity.similarity_with_concept("Hello", "greeting")
    # result2 = semantic_similarity.similarity_with_concept("Sandwitch", "greeting")
    # print(result, result1, result2)

    # result = semantic_similarity.similarity_with_concepts("I am religious", ["Islam", "humberger", "iphone"])
    # print(result)
