from programr.utils.logging.ylogger import YLogger
from programr.clients.client import BotClient

import os
from datetime import datetime
import yaml
from programr.services.service import ServiceFactory


class EventBotClient(BotClient):

    def __init__(self, id, argument_parser=None):
        self._running = False
        self._first_time = True
        super().__init__(id, argument_parser=argument_parser)

    def prior_to_run_loop(self):
        pass

    def run_loop(self):
        self._running = True

        # config = self.client_context.brain.configuration
        # self.client_context.brain.load_services(config)
        # mitsuku = ServiceFactory.get_service("mitsuku")
        # while self._running:
        #     message = input(">>")
        #     response = mitsuku.ask_question(bot.client.client_context, message)
        #     print(response)

        bot = self.bot_factory.bot("bot")
        bot.initiate_conversation_storage()

        while self._running:
            if self._first_time:
                client_context = self.client_context
                self._first_time = False

            session_number = 1
            username = "test_user"

            userid = client_context.userid
            client_context.bot.conversations[userid].set_property("session_number", session_number)
            client_context.bot.conversations[userid].set_property("username", username)

            # client_context.bot.facial_expression_recognition.append(-0.1)
            self._running = self.wait_and_answer(client_context)

            bot.save_conversation(client_context)

    def initial_question(self, request, username):
        question = "START SESSION " + str(request.session_number) + " " + username
        return question

    def dictionary_of_response(self, client_context, response):
        answer = ""
        image_filename = ""
        duration = ""
        video_filename = ""

        if client_context.bot.conversations[client_context.userid].answers:
            robot = client_context.bot.conversations[client_context.userid].answers[-1].robot["robot"]
        else:
            robot = None

        if robot:

            if robot is not None and "options" in robot and "option" in robot['options']:
                answer = robot['options']['option']

            if robot is not None and "image" in robot and "filename" in robot['image']:
                image_filename = robot['image']['filename']

            if robot is not None and "image" in robot and "duration" in robot["image"]:
                duration = robot["image"]["duration"]

            if robot is not None and "video" in robot and "filename" in robot["video"]:
                video_filename = robot["video"]["filename"]

        if len(client_context.bot.sentiment.values) > 0:
            try:
                if client_context.bot.configuration.emotive:
                    sentiment = client_context.bot.sentiment.final_sentiment_values[-1]
                else:
                    sentiment = -2.0
            except Exception as exep:
                sentiment = None
        else:
            sentiment = None

        # todo: added by hojjat, should be fixed
        if sentiment is None:
            sentiment = -2.0

        return {"conversation":
                    {"question": "",
                     "response": response,
                     "answer": answer,
                     "sentiment": sentiment,
                     },
                "image":
                    {"filename": image_filename,
                     "duration": duration
                     },
                "video":
                    {
                        "filename": video_filename
                    }
                }

    def wait_and_answer(self, client_context):
        raise NotImplementedError(
            "You must override this and implement the logic wait for a question and send an answer back")

    def post_run_loop(self):
        pass

    def run(self):
        raise NotImplementedError("You must override this and implement the logic")
        # root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        # filepath = os.path.join(root, "bots//ryan//config.yaml")
        # with open(filepath, encoding="utf-8") as file_reader:
        #     self._yaml_dict = yaml.load(file_reader)
        #
        # worker_running = self._yaml_dict["broker"]["running"]
        #
        # if self.arguments.noloop is False:
        #     YLogger.info(self, "Entering conversation loop...")
        #
        #     self.prior_to_run_loop()
        #
        #     if worker_running:
        #         self.worker_run_loop()
        #     else:
        #         self.run_loop()
        #
        #     self.post_run_loop()
        #
        # else:
        #     YLogger.debug(self, "noloop set to True, exiting...")
