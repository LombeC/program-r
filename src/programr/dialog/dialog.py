from programr.nlp.linguistic_features.sentence_segmentation import SentenceSegmentation
from programr.utils.logging.ylogger import YLogger
import re

from programr.parser.tokenizer import Tokenizer
from programr.utils.text.text import TextUtils


class Sentence(object):

    def __init__(self, nlp, text: str = None ):
        self._nlp = nlp
        self._tokenizer = self._nlp.tokenizer
        self._words = self._tokenizer.texts_to_words(text)
        self._response = None
        self._matched_context = None
        self._no_response = False

    @property
    def words(self):
        return self._words

    def append_word(self, word):
        self._words.append(word)

    def append_sentence(self, sentence):
        for word in sentence.words:
            self._words.append(word)

    def replace_words(self, text):
        self._words = self._split_into_words(text)

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, text: str):
        self._response = text

    @property
    def matched_context(self):
        return self._matched_context

    @matched_context.setter
    def matched_context(self, context):
        self._matched_context = context

    def num_words(self):
        return len(self.words)

    def word(self, num: int):
        if num < self.num_words():
            return self.words[num]
        return None

    def words_from_current_pos(self, current_pos: int):
        return self._tokenizer.words_from_current_pos(self._words, current_pos)

    def text(self):
        return self._tokenizer.words_to_texts(self._words)

    def _split_into_words(self, text):
        if text is None:
            return []
        return self._tokenizer.texts_to_words(text)


class Answer(object):
    def __init__(self, srai=False):
        self._srai = srai
        self._sentences = []
        self._properties = {}
        self._current_sentence_no = -1
        self.robot = {}

    @staticmethod
    def create_from_text(tokenizer, text, sentence_split_chars: str = ".", split=True, srai=False):
        answer = Answer(srai)
        if split is True:
            answer.split_into_sentences(text, sentence_split_chars, tokenizer)
        else:
            answer.sentences.append(Sentence(tokenizer, text))
        return answer

    @staticmethod
    def create_from_sentence(sentence: Sentence, srai=False):
        answer = Answer(srai)
        answer.sentences.append(sentence)
        return answer

    @staticmethod
    def create_from_sentences(sentences, srai=False):
        answer = Answer(srai)
        for sentence in sentences:
            answer = answer.create_from_sentence(sentence)

        return answer

    @property
    def sentences(self):
        return self._sentences


    def sentences_text(self):
        return '. '.join([sentence.text() for sentence in self._sentences])


    def sentence(self, num: int):
        if num < len(self._sentences):
            return self._sentences[num]
        raise Exception("Num sentence array violation !")




    def split_into_sentences(self, text: str, sentence_split_chars: str, tokenizer):
        if text is not None and text.strip():
            self._sentences = []
            all_sentences = text.split(sentence_split_chars)
            for each_sentence in all_sentences:
                if each_sentence.rstrip():
                    self._sentences.append(Sentence(tokenizer, each_sentence))


class Question(object):

    def __init__(self, srai=False):
        self._srai = srai
        self._sentences = []
        self._properties = {}
        self._current_sentence_no = -1


    #TODO Move sentence_split_charts into a property of tokenizer and move functionality into that class

    @staticmethod
    def create_from_text(nlp, text, split=True, srai=False):
        question = Question(srai)
        if split:
            for sentence_text in nlp.sentence_segmentation.segment(text):
                question.sentences.append(Sentence(nlp, sentence_text))
        else:
            pass
            #question.sentences.append(Sentence(tokenizer, text))
        return question

    @staticmethod
    def create_from_sentence(sentence: Sentence, srai=False):
        question = Question(srai)
        question.sentences.append(sentence)
        return question

    @staticmethod
    def create_from_question(question, srai=False):
        new_question = Question(srai)
        for each_sentence in question.sentences:
            new_question.sentences.append(each_sentence)
        return new_question

    def debug_info(self):
        str = ""
        for sentence in self._sentences:
            str += sentence.text()
            str += " = "
            if sentence.response is not None:
                str += sentence.response
            else:
                str += "N/A"
            str += ", "
        return str

    @property
    def sentences(self):
        return self._sentences

    def has_response(self):
        for sentence in self._sentences:
            if sentence.response is not None:
                return True
        return False

    def set_current_sentence_no(self, sentence_no):
        self._current_sentence_no = sentence_no

    def set_property(self, name: str, value: str):
        self._properties[name] = value

    def property(self, name: str):
        if name in self._properties:
            return self._properties[name]
        return None

    def sentence(self, num: int):
        if num < len(self._sentences):
            return self._sentences[num]
        raise Exception("Num sentence array violation !")

    def current_sentence(self):
        if not self._sentences:
            raise Exception("Num sentence array violation !")
        return self._sentences[self._current_sentence_no]

    def previous_nth_sentence(self, num):
        # print("sentences in conversation: {}".format(self._sentences))
        if len(self._sentences) < num:
            print("size of sentences array: " + str(len(self._sentences)))
            for sentences in self._sentences:
                print("contents of sentences array: " + str(sentences.words))
            raise Exception("Num sentence array violation !")
        previous = -1 - num
        return self._sentences[previous]

    def combine_sentences(self):
        return ". ".join([sentence.text() for sentence in self._sentences])

    def combine_answers(self):
        return ". ".join([sentence.response for sentence in self.sentences if sentence.response is not None])

    def split_into_sentences(self, text: str, sentence_split_chars: str, tokenizer):
        if text is not None and text.strip():
            self._sentences = []
            all_sentences = text.split(sentence_split_chars)
            for each_sentence in all_sentences:
                self._sentences.append(Sentence(tokenizer, each_sentence))


#
# A Conversation is made up of questions, each question is made up of sentences
#
class Conversation(object):

    def __init__(self, client_context):
        self._sentence_segmentation = client_context.brain.nlp.sentence_segmentation
        self._client_context = client_context
        self._questions = []
        self._answers = []
        self._max_histories = client_context.bot.configuration.conversations.max_histories
        self._properties = {'topic': client_context.bot.configuration.conversations.initial_topic}


    @property
    def answers(self):
        return self._answers

    @property
    def questions(self):
        return self._questions

    @property
    def max_histories(self):
        return self._max_histories

    @property
    def properties(self):
        return self._properties

    def has_current_question(self):
        return bool(self._questions)

    def current_question(self):
        if self._questions:
            return self._questions[-1]
        raise Exception("Invalid question index")

    def previous_nth_question(self, num: int):
        # print("questions: {}".format(self._questions))
        if len(self._questions) < num:
            raise Exception("Num question array violation !")
        previous = -1 - num
        return self._questions[previous]

    def set_property(self, name: str, value: str):
        # TODO: Need to save self._properties to database with user info
        if name == 'topic':
            if value == "":
                value = '*'
        self._properties[name] = value

    def set_properties(self, properties):
        for key in properties:
            self._properties[key] = properties[key]

    def property(self, name: str):
        if self._properties is not None:
            if name in self._properties:
                return self._properties[name]
        return None

    def record_question(self, question: Question):
        if len(self._questions) == self._max_histories:
            YLogger.info(self, "Conversation history at max [%d], removing oldest question", self._max_histories)
            self._questions.remove(self._questions[0])
        self._questions.append(question)


    def record_answer(self, answer):
        if len(self._answers) == self._max_histories:
            YLogger.info(self, "Conversation history at max [%d], removing oldest answer", self._max_histories)
            self._answers.remove(self._answers[0])
        self._answers.append(answer)


    def pop_dialog(self):
        if self._questions:
            self._questions.pop()

    def load_initial_variables(self, variables_collection):
        for pair in variables_collection.pairs:
            YLogger.debug(self, "Setting variable [%s] = [%s]", pair[0], pair[1])
            self._properties[pair[0]] = pair[1]

    def get_topic_pattern(self, client_context):
        topic_pattern = self.property("topic")

        if topic_pattern is None:
            YLogger.info(client_context, "No Topic pattern default to [*]")
            topic_pattern = "*"
        else:
            YLogger.info(client_context, "Topic pattern = [%s]", topic_pattern)

        return topic_pattern

    def parse_last_sentences_from_response(self, response):
        # TODO Issue here when the response is more than just a simple sentence
        # If the response contains punctuation such as "Hello. There" then THAT is none
        # response = re.sub(r'<\s*br\s*/>\s*', ".", response)
        # response = re.sub(r'<br></br>*', ".", response)
        # sentences = response.split(".")
        # sentences = [x for x in sentences if x]
        # last_sentence = sentences[-1]
        # #TODO uncomment the code below
        # #that_pattern = TextUtils.strip_all_punctuation(last_sentence)
        # that_pattern = last_sentence
        # that_pattern = that_pattern.strip().strip("?")
        # # TODO Added this to catch a failed sentence
        # if that_pattern == "":
        #     that_pattern = '*'
        # return that_pattern

        #todo work on this part to make it cleaner
        if "(" in response:
            response = response.split("(")[0]
        else:
            if "#" in response:
                response = response.split("#")[0]

        # doc = self._nlp(response)
        # sentences = list(doc.sents)
        # last_sentence = sentences[-1].text

        sentences = self._sentence_segmentation.segment(response)
        last_sentence = sentences[-1]
        that_pattern = last_sentence.strip()#.strip("?")
        if that_pattern == "":
            that_pattern = "*"
        return that_pattern



    def get_that_pattern(self, client_context, srai=False):
        try:
            that_question = None
            if srai is False:
                that_question = self.previous_nth_question(1)
            else:
                if len(self._questions) > 2:
                    for question in reversed(self._questions[:-2]):
                        if question._srai is False and question.has_response():
                            that_question = question
                            break

            if that_question is not None:
                that_sentence = that_question.current_sentence()
            else:
                that_sentence = None

            # If the last response was valid, i.e not none and not empty string, then use
            # that as the that_pattern, otherwise we default to '*' as pattern
            if that_sentence.response is not None and that_sentence.response != '':
                that_pattern = self.parse_last_sentences_from_response(that_sentence.response)
                YLogger.info(client_context, "That pattern = [%s]", that_pattern)
            else:
                YLogger.info(client_context, "That pattern, no response, default to [*]")
                that_pattern = "*"

        except Exception as e:
            YLogger.info(client_context, "No That pattern default to [*]")
            that_pattern = "*"

        return that_pattern