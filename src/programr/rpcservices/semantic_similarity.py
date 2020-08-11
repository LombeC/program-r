import torch
import numpy as np

from transformers import RobertaTokenizer, RobertaForSequenceClassification, InputExample, glue_convert_examples_to_features

from programr.utils.logging.ylogger import YLogger
from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration

class SemanticSimilarity():

    def __init__(self):
        pass

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