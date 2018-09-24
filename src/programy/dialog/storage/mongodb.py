from programy.config.bot.mongodbstorage import BotConversationsMongodbStorageConfiguration
from programy.dialog.storage.base import ConversationStorage
from programy.utils.logging.ylogger import YLogger
import datetime
import pymongo
from pymongo import MongoClient, IndexModel

class ConversationMongodbStorage(ConversationStorage):

    def __init__(self, config: BotConversationsMongodbStorageConfiguration):
        ConversationStorage.__init__(self, config)
        client = MongoClient()
        self._config = config
        if not config.name in client.list_database_names():
            YLogger.info(self, "Database doesn't exist make a new one!")

        self.db = client[config.name]



    def save_conversation(self, client_context):
        userid = client_context.userid
        bot_properties = client_context.bot.conversations[userid].properties
        questions = client_context.bot.conversations[userid].questions
        answers = client_context.bot.conversations[userid].answers
        try:
            last_question = questions[-1].sentences
        except Exception as e:
            YLogger.exception(self, "question sentences length is zero", e)
            raise e

        try:
            # todo this doesn't handle good when sentence is empty
            last_answer = answers[-1].sentences
        except Exception as e:
            YLogger.exception(self, "answer sentences length is zero", e)
            raise e

        try:
            image_filename = answers[-1].robot['robot']['image']['filename']
        except Exception as e:
            image_filename = None

        try:
            duration = answers[-1].robot['robot']['image']['duration']
        except Exception as e:
            duration = None

        try:
            video_filename = answers[-1].robot['robot']['video']['filename']
        except Exception as e:
            video_filename = None


        try:
            session_number = bot_properties["session_number"]
        except Exception as e:
            session_number = None

        try:
            username = bot_properties["username"]
        except Exception as e:
            username = None

        question_sentence_text, answer_sentence_text = self.create_conversation(last_question, last_answer)


        document = {"conversation": {
            "question": question_sentence_text,
            "answer": answer_sentence_text,
            "timestamp": datetime.datetime.now()
            },

            "session_info": {
                "session_number": session_number ,
                "username": username
            },

            "image": {
                "filename": image_filename,
                "duration": duration,
            },

            "video": {
                "filename": video_filename
            }

        }

        self.db[self._config.collection_name].insert_one(document)


    def load_conversation(self, conversation, clientid, restore_last_topic=False):
        #todo needs loading the whole conversation with properties
        #needs more work
        pass

    def empty(self):
        self.db[self._config.collection_name].drop()




    def create_conversation(self, question, answer):
        question_sentence_text = ""
        for question_sentence in question:
            try:
                if question_sentence.words[-1].endswith('?') or question_sentence.words[-1].endswith(')'):
                    end_sign = ""
                else:
                    end_sign = ". "
            except Exception as e:
                YLogger.exception(self, "Failed to get end_sign ", e)

            question_sentence_text += " ".join(question_sentence.words) +end_sign

        answer_sentence_text = ""
        for answer_sentence in answer:
            try:
                if answer_sentence.words[-1].endswith('?') or answer_sentence.words[-1].endswith(')'):
                    end_sign = ""
                else:
                    end_sign = ". "
            except Exception as e:
                YLogger.exception(self, "Failed to get end_sign ", e)

            answer_sentence_text += " ".join(answer_sentence.words) + end_sign

        return question_sentence_text, answer_sentence_text