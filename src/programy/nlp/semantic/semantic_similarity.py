import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import time
from programy.utils.logging.ylogger import YLogger


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
        super().__init__()
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"
        t1 = time.time()
        embed = hub.Module(module_url)
        self.similarity_input_placeholder = tf.placeholder(tf.string, shape=(None))
        self.similarity_message_encodings = embed(self.similarity_input_placeholder)
        self.session = tf.Session()
        t2 = time.time()
        self.session.run(tf.global_variables_initializer())
        t3 = time.time()
        self.session.run(tf.tables_initializer())
        t4 = time.time()
        print(t2 - t1)
        print(t3 - t2)
        print(t4 - t3)

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


class DefaultSemanticSimilarity(SemanticSimilarity):

    def __init__(self):
        pass

    def similarity_with_concept(self, text, concept):
        pass

    def similarity_with_concepts(self, text, concepts):
        pass



if __name__ == "__main__":
    semantic_similarity = EmbeddingSemanticSimilarity()
    result = semantic_similarity.similarity_with_concept("Hi", "greeting")
    result1 = semantic_similarity.similarity_with_concept("Hello", "greeting")
    result2 = semantic_similarity.similarity_with_concept("Sandwitch", "greeting")
    print(result, result1, result2)

    # result = semantic_similarity.similarity_with_concepts("I am religious", ["Islam", "humberger", "iphone"])
    # print(result)
