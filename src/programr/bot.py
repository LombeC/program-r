import logging

from programr.robot.facial_expression_recognition import FacialExpressionRecognition
from programr.robot.sentimentdata import SentimentData
from programr.utils.logging.ylogger import YLogger

from programr.brain import Brain
from programr.dialog.dialog import Conversation, Question, Answer, Sentence
from programr.dialog.storage.factory import ConversationStorageFactory
from programr.config.bot.bot import BotConfiguration
from programr.utils.classes.loader import ClassLoader

try:
    import _pickle as pickle
except:
    import pickle

import numpy as np
import os

class BrainSelector(object):

    def __init__(self, configuration):
        self._configuration = configuration

    def select_brain(self, brains):
        pass


class DefaultBrainSelector(BrainSelector):

    def __init__(self, configuration):
        BrainSelector.__init__(self, configuration)

    def select_brain(self, brains):
        if brains:
            return next (iter (brains.values()))
        return None


class BrainFactory(object):

    def __init__(self, bot):
        self._brains = {}
        self.loads_brains(bot)
        self._brain_selector = None
        self.load_brain_selector(bot.configuration)

    def brainids(self):
        return self._brains.keys()

    def brain(self, id):
        if id in self._brains:
            return self._brains[id]
        else:
            return None

    def loads_brains(self, bot):
        for config in bot.configuration.configurations:
            brain = Brain(bot, config)
            self._brains[brain.id] = brain

    def load_brain_selector(self, configuration):
        if configuration.brain_selector is None:
            self._brain_selector = DefaultBrainSelector(configuration)
        else:
            try:
                self._brain_selector = ClassLoader.instantiate_class(configuration.brain_selector)(configuration)
            except Exception as e:
                self._brain_selector = DefaultBrainSelector(configuration)

    def select_brain(self):
        return self._brain_selector.select_brain(self._brains)


class Bot(object):

    def __init__(self, config: BotConfiguration, client=None):
        self._configuration = config
        self._client = client

        self._brain_factory = BrainFactory(self)

        self._question_depth = 0
        self._question_start_time = None

        self._spell_checker = None
        self.initiate_spellchecker()

        self._rephase_clauses = []

        self._conversations = {}
        self._conversation_storage = None
        self._corenlp = None

        self._facial_expression_recognition = FacialExpressionRecognition()

        self._sentiment_data = SentimentData()

        self.initiate_conversation_storage()

    def ylogger_type(self):
        return "bot"

    @property
    def id(self):
        return self._configuration.section_name

    @property
    def client(self):
        return self._client

    @property
    def configuration(self):
        return self._configuration

    @property
    def corenlp(self):
        return self._corenlp

    @property
    def facial_expression_recognition(self):
        return self._facial_expression_recognition

    @property
    def sentiment(self):
        return self._sentiment_data

    @property
    def brain_factory(self):
        return self._brain_factory

    def initiate_spellchecker(self):
        # TODO Move this to Spelling bass class
        if self.configuration is not None:
            if self.configuration.spelling.classname is not None:
                try:
                    YLogger.info(self, "Loading spelling checker from class [%s]", self.configuration.spelling.classname)
                    spell_class = ClassLoader.instantiate_class(self.configuration.spelling.classname)
                    self._spell_checker = spell_class(self.configuration.spelling)
                except Exception as excep:
                    YLogger.exception(self, "Failed to initiate spellcheker", excep)
            else:
                YLogger.warning(self, "No configuration setting for spelling checker!")


    def set_conversation_question(self, client_context, questions):
        self._conversations[client_context.userid]._questions = questions



    @property
    def spell_checker(self):
        return self._spell_checker

    @property
    def brain(self):
        return self._brain_factory.select_brain()

    @property
    def conversations(self):
        return self._conversations

    @property
    def default_response(self):
        if self.configuration is not None:
            return self.configuration.default_response
        return BotConfiguration.DEFAULT_RESPONSE

    @property
    def default_response_srai(self):
        if self.configuration is not None:
            return self.configuration.default_response_srai
        return None

    @property
    def exit_response(self):
        if self.configuration is not None:
            return self.configuration.exit_response
        return BotConfiguration.DEFAULT_EXIT_RESPONSE

    @property
    def exit_response_srai(self):
        if self.configuration is not None:
            return self.configuration.exit_response_srai
        return BotConfiguration.DEFAULT_EXIT_RESPONSE_SRAI

    @property
    def initial_question(self):
        if self.configuration is not None:
            return self.configuration.initial_question
        return BotConfiguration.DEFAULT_INITIAL_QUESTION

    @property
    def rephrase_clauses(self):
        if self.configuration is not None:
            if len(self._rephase_clauses)==0:
                rephrase_file = self.configuration.rephrase_clauses_file.replace("$BOT_ROOT", self.client.arguments.bot_root)
                with open(rephrase_file) as file_reader:
                    for line in file_reader:
                        line = line.rstrip()
                        if not line.endswith("."):
                            line = line+"."
                        self._rephase_clauses.append(line)
                return self._rephase_clauses
            else:
                return self._rephase_clauses
        else:
            return [""]

    @property
    def initial_question_srai(self):
        if self.configuration is not None:
            return self.configuration.initial_question_srai
        return BotConfiguration.DEFAULT_INITIAL_QUESTION_SRAI

    @property
    def override_properties(self):
        if self.configuration is not None:
            return self.configuration.override_properties
        return False

    def get_version_string(self, client_context):
        if client_context.brain.properties.has_property("version"):
            # The old version of returning the version string, did not distinquish
            # between App and Grammar version
            return "%s, v%s, initiated %s" % (
                client_context.brain.properties.property("name"),
                client_context.brain.properties.property("version"),
                client_context.brain.properties.property("birthdate"))
        else:
            # This version now does
            return "%s, App: v%s Grammar v%s, initiated %s" % (
                client_context.brain.properties.property("name"),
                client_context.brain.properties.property("app_version"),
                client_context.brain.properties.property("grammar_version"),
                client_context.brain.properties.property("birthdate"))

    def has_conversation(self, client_context):
        return bool(client_context.userid in self._conversations)

    def conversation(self, client_context):
        return self.get_conversation(client_context)

    def get_conversation(self, client_context):
        # TODO move this to Conversations base class
        if client_context.userid in self._conversations:
            YLogger.info(client_context, "Retrieving conversation for client %s", client_context.userid)
            return self._conversations[client_context.userid]

        else:
            YLogger.info(client_context, "Creating new conversation for client %s", client_context.userid)

            conversation = Conversation(client_context)

            if client_context.brain.properties is not None:
                conversation.load_initial_variables(client_context.brain.variables)

            self._conversations[client_context.userid] = conversation

            self.load_conversation(client_context.userid)

            return conversation

    def initiate_conversation_storage(self):
        if self.configuration is not None:
            if self.configuration.conversations is not None:
                self._conversation_storage = ConversationStorageFactory.get_storage(self.configuration)
                if self._conversation_storage is not None:
                    if self.configuration.conversations.empty_on_start is True:
                        self._conversation_storage.empty()

    def load_conversation(self, clientid):
        if self._conversation_storage is not None:
            if clientid in self._conversations:
                conversation = self._conversations[clientid]
                self._conversation_storage.load_conversation(conversation, clientid,
                                                             self.configuration.conversations.restore_last_topic)

    def load_client_properties(self):
        if self._conversation_storage is not None:
            return self._conversation_storage.load_client_properties()

    def save_conversation(self, client_context):
        if self._conversation_storage is not None:
            if client_context.userid in self._conversations:
                self._conversation_storage.save_conversation(client_context)
            else:
                YLogger.error(self, "Unknown conversation id type [%s] unable tonot persist!", client_context.userid)

    def check_spelling_before(self, each_sentence):
        # TODO Move this to spelliing base class
        if self.configuration.spelling.check_before is True:
            text = each_sentence.text()
            corrected = self.spell_checker.correct(text)
            YLogger.debug(self, "Spell Checker corrected [%s] to [%s]", text, corrected)
            each_sentence.replace_words(corrected)

    def check_spelling_and_retry(self, client_context, each_sentence):
        # TODO Move this to spelling base class
        if self.configuration.spelling.check_and_retry is True:
            text = each_sentence.text()
            corrected = self.spell_checker.correct(text)
            YLogger.debug(self, "Spell Checker corrected [%s] to [%s]", text, corrected)
            each_sentence.replace_words(corrected)
            response = client_context.brain.ask_question(client_context, each_sentence)
            return response
        return None

    def get_default_response(self, client_context):
        try:
            rephrased_clauses = client_context.bot.rephrase_clauses
            last_question = client_context.bot._conversations[client_context.userid].questions[-2]
            last_sentence = last_question.sentences[-1]

            r = np.random.randint(0, len(rephrased_clauses), 1)[0]

            results = [last_sentence.response.startswith(sentence) for sentence in rephrased_clauses]

            if any(results):
                sentences = last_sentence.response.split(".")
                response = ". ".join(sentences[1:])
                response = response.split('.')[-1]
                response = rephrased_clauses[r] + " "+response
            else:
                response = rephrased_clauses[r] + " " + last_sentence.response.split(".")[-1]

        except:
            response= self.default_response
        return response

    def get_initial_question(self, client_context):
        if self.initial_question_srai is not None:
            sentence = Sentence(client_context.brain.nlp, self.initial_question_srai)
            initial_question = client_context.brain.ask_question(client_context, sentence)
            if initial_question is None or not initial_question:
                initial_question = self.initial_question
            return initial_question
        else:
            return self.initial_question

    def get_exit_response(self, client_context):
        if self.exit_response_srai is not None:
            sentence = Sentence(client_context.brain.nlp, self.exit_response_srai)
            exit_response = client_context.brain.ask_question(client_context, sentence)
            if exit_response is None or not exit_response:
                exit_response = self.exit_response
            return exit_response
        else:
            return self.exit_response

    def pre_process_text(self, client_context, text, srai):
        text = text.upper()
        if srai is False:
            pre_processed = client_context.brain.pre_process_question(client_context, text)
            YLogger.debug(client_context, "Pre Processed (%s): %s", client_context.userid, pre_processed)
        else:
            pre_processed = text

        if pre_processed is None or pre_processed == "":
            pre_processed = self.configuration.empty_string

        return pre_processed

    def get_question(self, client_context, pre_processed, srai):

        if srai is False:
            #return Question.create_from_text(client_context.brain.tokenizer, pre_processed, srai=srai)
            return Question.create_from_text(client_context.brain.nlp, pre_processed, srai=srai)
        else:
            return Question.create_from_text(client_context.brain.nlp, pre_processed, srai=srai)


    def get_answer(self, client_context, pre_processed, srai=False):
        pre_processed = ". ".join(pre_processed)
        if srai is False:
            return Answer.create_from_text(client_context.brain.nlp.tokenizer, pre_processed, srai=srai)
        else:
            return Answer.create_from_text(client_context.brain.nlp.tokenizer, pre_processed, split=False, srai=srai)


    def combine_answers(self, answers):
        return ". ".join([sentence for sentence in answers if sentence is not None])

    def post_process_response(self, client_context, response, srai):
        if srai is False:
            answer = client_context.brain.post_process_response(client_context, response).strip()
            if not answer:
                answer = self.get_default_response(client_context)
        else:
            answer = response
        return answer

    def log_answer(self, client_context, text, answer, responselogger):
        YLogger.debug(client_context, "Processed Response (%s): %s", client_context.userid, answer)

        if responselogger is not None:
            responselogger.log_response(text, answer)

    def ask_question(self, client_context, text, srai=False, responselogger=None):

        # if srai is False:
        #     client_context.bot = self
        #     client_context.brain = client_context.bot.brain

        client_context.mark_question_start(text)

        pre_processed = self.pre_process_text(client_context, text, srai)

        question = self.get_question(client_context, pre_processed, srai)

        conversation = self.get_conversation(client_context)

        conversation.record_question(question)

        answer_sentences = []
        sentence_no = 0
        for sentence in question.sentences:
            question.set_current_sentence_no(sentence_no)
            answer_sentence, options = self.process_sentence(client_context, sentence, srai, responselogger)
            answer_sentences.append(answer_sentence)
            sentence_no += 1

        # sentence = Sentence(client_context.brain.nlp, pre_processed)
        # answer_sentence = self.process_sentence(client_context, sentence, srai, responselogger)
        # answer_sentences = [answer_sentence]

        answer = Answer.create_from_sentences(answer_sentences, srai)
        conversation.record_answer(answer)


        client_context.reset_question()

        #TODO this part of code added by rohola
        # each time we save the last conversation, loads happen just in the run_loop
        # file_obj = open("/home/rohola/conv_questions.p", 'wb')
        # pickle.dump(conversation.questions, file_obj)

        if srai is True:
            conversation.pop_dialog()


        response = answer.sentences_text()

        self.log_question_and_answer(client_context, text, response)

        return response


    def ask_question_with_options(self, client_context, text, srai=False, responselogger=None):

        # if srai is False:
        #     client_context.bot = self
        #     client_context.brain = client_context.bot.brain



        client_context.mark_question_start(text)

        pre_processed = self.pre_process_text(client_context, text, srai)

        question = self.get_question(client_context, pre_processed, srai)

        conversation = self.get_conversation(client_context)

        conversation.record_question(question)


        answer_sentences = []
        sentence_no = 0
        options = []
        for sentence in question.sentences:
            question.set_current_sentence_no(sentence_no)
            answer_sentence, option = self.process_sentence_with_options(client_context, sentence, srai, responselogger)
            answer_sentences.append(answer_sentence)
            options.append(option)
            sentence_no += 1

        #answer = self.get_answer(client_context, answers)
        answer = Answer.create_from_sentences(answer_sentences, srai)
        answer.robot = options
        conversation.record_answer(answer)

        if len(self.conversations[client_context.userid].answers) != len(self.sentiment.values):
            self.sentiment.append_sentiment(None)
            self.sentiment.append_sentiment_distribution([])
            self.sentiment.append_final_sentiment(None)

        client_context.reset_question()

        # we just save when it's needed by the session_saving_mode flag, NOT EVERY TIME
        if self.configuration.session.session_saving_mode:
            self.save_session(client_context, conversation)

        if srai is True:
            conversation.pop_dialog()

        response = answer.sentences_text()

        self.log_question_and_answer(client_context, text, response)

        return response, options


    def save_session(self, client_context, conversation):
        saving_dir = client_context.bot.configuration.session.session_saving_dir
        question_save_dir = os.path.join(saving_dir, "questions.p")
        properties_save_dir = os.path.join(saving_dir, "properties.p")
        questions_pickle_file = open(question_save_dir, 'wb')
        properties_pickle_file = open(properties_save_dir, 'wb')
        pickle.dump(conversation.questions, questions_pickle_file)
        pickle.dump(conversation.properties, properties_pickle_file)
        

    def log_question_and_answer(self, client_context, text, response):
        convo_logger = logging.getLogger("conversation")
        if convo_logger:
            qanda =  "%s - Question[%s], Response[%s]"%(str(client_context), text, response)
            convo_logger.info(qanda)

    def process_sentence(self, client_context, sentence, srai, responselogger):

        client_context.check_max_recursion()
        #TODO uncomment the line below
        #client_context.check_max_timeout()

        if srai is False:
            self.check_spelling_before(sentence)


        response = client_context.brain.ask_question(client_context, sentence, srai)
        #response = client_context.brain.ask_question_with_options(client_context, sentence, srai)

        if response is None and srai is False:
            response = self.check_spelling_and_retry(client_context, sentence)

        if response is not None:
            return self.handle_response(client_context, sentence, response, srai, responselogger)
        else:
            #raise("Error")
            return self.handle_none_response(client_context, sentence, responselogger)

        return answer

    def process_sentence_with_options(self, client_context, sentence, srai, responselogger):
        client_context.check_max_recursion()

        if srai is False:
            self.check_spelling_before(sentence)

        response, options = client_context.brain.ask_question_with_options(client_context, sentence, srai)

        if response is None and srai is False:
            response = self.check_spelling_and_retry(client_context, sentence)

        if response is not None:
            return self.handle_response(client_context, sentence, response, srai, responselogger, options)
        else:
            return self.handle_none_response(client_context, sentence, responselogger, options)   


    def handle_response(self, client_context, sentence, response, srai, responselogger, options=[]):
        YLogger.debug(client_context, "Raw Response (%s): %s", client_context.userid, response)
        YLogger.debug(client_context, "Options (%s)", options)
        sentence.response = response
        post_processed_response = self.post_process_response(client_context, response, srai)
        response_sentence = Sentence(client_context.brain.nlp, post_processed_response)
        response_text = response_sentence.text()
        self.log_answer(client_context, sentence.text, response_text, responselogger)
        if len(options) == 0:
            return response_sentence, None
        else:
            YLogger.debug(client_context, "Returning response_sentence and options.")
            return response_sentence, options

    def handle_none_response(self, client_context, sentence, responselogger, options = []):
        sentence.response = self.get_default_response(client_context)
        non_hanlde_sentence = Sentence(client_context.brain.nlp, sentence.response)
        non_hanlde_sentence._no_response = True

        if responselogger is not None:
            responselogger.log_unknown_response(non_hanlde_sentence)

        if len(options)==0:
            return non_hanlde_sentence
        else:
            return non_hanlde_sentence, options