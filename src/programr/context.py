import datetime
import uuid

from programr.utils.logging.ylogger import YLogger

class ClientContext(object):
    
    def __init__(self, client, userid):
        self._client = client
        self._userid = userid
        self._bot = None
        self._brain = None
        self._question_start_time = None
        self._question_depth = 0
        self._id = uuid.uuid1()

        self.user_name = "Unknown"
        self.location = "Unknown"
        self.time_zone = "Unknown"

    def ylogger_type(self):
        return "context"

    @property
    def id(self):
        return self._id

    @property
    def client(self):
        return self._client

    @property
    def userid(self):
        return self._userid

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, id):
        self._bot = id

    @property
    def brain(self):
        return self._brain

    @brain.setter
    def brain(self, id):
        self._brain = id

    def load_client_properties(self, user_name, location, time_zone):
        self.user_name = user_name
        self.location = location
        self.time_zone = time_zone

    def get_user_name(self):
        return self.user_name

    def get_location(self):
        return self.location

    def get_time_zone(self):
        return self.time_zone

    def check_max_recursion(self):
        if self.bot.configuration.max_question_recursion != -1:
            if self._question_depth > self.bot.configuration.max_question_recursion:
                raise Exception("Maximum recursion limit [%d] exceeded" % self.bot.configuration.max_question_recursion)

    def total_search_time(self):
        delta = datetime.datetime.now() - self._question_start_time
        return abs(delta.total_seconds())

    def check_max_timeout(self):
        if self.bot.configuration.max_question_timeout != -1:
            if self.total_search_time() >= self.bot.configuration.max_question_timeout:
                raise Exception("Maximum search time limit [%d] exceeded" % self.bot.configuration.max_question_timeout)

    def mark_question_start(self, question):
        YLogger.debug(self, "##########################################################################################")
        YLogger.debug(self, "Question (%s): %s", self._client.id, question)

        if self._question_depth == 0:
            self._question_start_time = datetime.datetime.now()
            
        self._question_depth += 1

    def reset_question(self):
        self._question_depth = 0

    def __str__(self):
        return "[%s] [%s] [%s] [%s] [%d]"% (
            self._client.id,
            self._userid,
            self._bot.id if self._bot else "",
            self._brain.id if self._brain else "",
            self._question_depth
        )