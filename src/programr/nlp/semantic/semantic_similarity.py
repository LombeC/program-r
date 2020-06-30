import numpy as np
import time
import torch

from programr.utils.logging.ylogger import YLogger
from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, TextClassificationPipeline, RobertaModel, DistilBertModel, AutoTokenizer, AutoModel

class SemanticSimilarity():

    def __init__(self):
        pass

    @staticmethod
    def factory(type_):
        if type_ == "embedding":
            return EmbeddingSemanticSimilarity()

        elif type_ == "default":
            return DefaultSemanticSimilarity()

        else:
            YLogger.warning(DefaultSemanticSimilarity, "the module is unknown, defaulting to DefaultSemanticSimilarity")
            return DefaultSemanticSimilarity()

    def similarity_with_concepts(self, text, concepts):
        raise NotImplementedError("Should be override to be used.")

    def similarity_with_concept(self, text, concept):
        raise NotImplementedError("")


class EmbeddingSemanticSimilarity(SemanticSimilarity):

    def __init__(self):
        ## todo we need to re-implement the semantic similarity with torch, tf is no longer supported in programr
        pass
        # super().__init__()
        # module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        # t1 = time.time()
        # embed = hub.Module(module_url)
        # self.similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        # self.similarity_message_encodings = embed(self.similarity_input_placeholder)
        # self.session = tf.Session()
        # t2 = time.time()
        # self.session.run(tf.global_variables_initializer())
        # t3 = time.time()
        # self.session.run(tf.tables_initializer())
        # t4 = time.time()
        # print(t2 - t1)
        # print(t3 - t2)
        # print(t4 - t3)

    def similarity_with_concepts(self, text, concepts):
        text_embedding = self.session.run(self.similarity_message_encodings,
                                          feed_dict={self.similarity_input_placeholder: [text]})

        concepts_embedding = self.session.run(self.similarity_message_encodings,
                                              feed_dict={self.similarity_input_placeholder: concepts})

        similarity_scores = np.inner(text_embedding, concepts_embedding)[0].tolist()

        return similarity_scores

    def similarity_with_concept(self, text, concept):
        text_embedding = self.session.run(self.similarity_message_encodings,
                                          feed_dict={self.similarity_input_placeholder: [text]})

        concept_embedding = self.session.run(self.similarity_message_encodings,
                                             feed_dict={self.similarity_input_placeholder: [concept]})

        similarity_score = np.inner(concept_embedding, text_embedding)[0][0]

        return similarity_score

# TODO: Implement this class as the torch version of above class
class PyTorchSemanticSimilarity(SemanticSimilarity):
    
    def __init__(self, semantic_similarity_config: BrainSemanticSimilarityConfiguration):
        super().__init__()
        self.semantic_similarity_config = semantic_similarity_config
        # model_dir = semantic_similarity_config.model_dir
        model_dir = 'distilroberta-base'
        tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
        model = RobertaModel.from_pretrained(model_dir)
        

        self.similarity_classifier = SemanticClassifer(model, tokenizer)

    def similarity_with_concept(self, text, concept):
        pass

    def similarity_with_concepts(self, text, concepts):
        pass

class DefaultSemanticSimilarity(SemanticSimilarity):

    def __init__(self):
        pass

    def similarity_with_concept(self, text, concept):
        pass

    def similarity_with_concepts(self, text, concepts):
        pass


class SemanticClassifer:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def __call__(self, text):
        input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)
        outputs = model(input_ids)
        last_hidden_states = outputs[0]  # The last hidden-state is the first element of the output tuple   

        # input_ids = torch.tensor(self.tokenizer.encode(text, add_special_tokens=True)).unsqueeze(0)
        # outputs = self.model(input_ids)
        # outputs = outputs[0].detach().numpy()
        # scores = np.exp(outputs) / np.exp(outputs).sum(-1)
        # scores = scores[0].tolist()
        # result = {"negative": scores[0], "neutral": scores[1], "positive": scores[2]}
        # return result



if __name__ == "__main__":
    # NOTE: Example of loading in roberta model
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased')
    model = RobertaModel.from_pretrained('distilroberta-base')
    input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute")).unsqueeze(0)
    outputs = model(input_ids)
    print(outputs)

    # tokenizer = AutoTokenizer.from_pretrained('/home/jarid/.cache/torch/transformers')
    # model = AutoModel.from_pretrained('/home/jarid/.cache/torch/transformers')
    # input_ids = torch.tensor(tokenizer.encode("Hello, my dog is cute")).unsqueeze(0)
    # outputs = model(input_ids)
    # print(outputs)
    
    # NOTE: Tensorflow version
    # semantic_similarity = EmbeddingSemanticSimilarity()
    # result = semantic_similarity.similarity_with_concept("Hi", "greeting")
    # result1 = semantic_similarity.similarity_with_concept("Hello", "greeting")
    # result2 = semantic_similarity.similarity_with_concept("Sandwitch", "greeting")
    # print(result, result1, result2)

    # result = semantic_similarity.similarity_with_concepts("I am religious", ["Islam", "humberger", "iphone"])
    # print(result)
