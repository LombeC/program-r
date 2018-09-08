from programy.utils.logging.ylogger import YLogger

from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.exceptions import ParserException

from programy.nlp.semantic.semantic_similarity import SemanticSimilarity

class PatternConceptNode(PatternNode):


    def __init__(self, attribs, text, userid='*'):
        PatternNode.__init__(self, userid)
        if 'name' in attribs:
            self._concept_name = attribs['name'].upper()
        elif text:
            self._concept_name = text.upper()
        else:
            raise ParserException("Invalid concept node, no name specified as attribute or text")


    @property
    def concept_name(self):
        return self._concept_name

    def is_set(self):
        return False

    def to_xml(self, client_context, include_user=False):
        #todo needs to be implemented
        raise Exception("Needs to be implemented")



    def equals(self, client_context, words, word_no):
        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)


        last_index = words.words.index("__TOPIC__")
        sentence = words.words[:last_index]
        if sentence:
            concepts = self._concept_name.split("|")
            this_concept = concepts[0]  # this is the main concept we have to compare others to
            other_concepts = concepts[1:]  # this is other concepts we have to compare this_concept to

            sentence_text = " ".join(sentence)

            similarity_with_this_concept = client_context.brain.nlp.semantic_similarity.similarity_with_concept(sentence_text, this_concept)
            similarity_with_other_concepts = client_context.brain.nlp.semantic_similarity.similarity_with_concepts(sentence_text, other_concepts)

            if similarity_with_this_concept > max(similarity_with_other_concepts):
                result = True
            else:
                result = False
            word_no = word_no + len(sentence) - 1
        else:
            result = True

        return EqualsMatch(result, word_no, word)

