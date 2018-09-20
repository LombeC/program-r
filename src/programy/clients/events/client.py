from programy.utils.logging.ylogger import YLogger
from programy.clients.client import BotClient

import os
from datetime import datetime
import yaml
from programy.services.service import ServiceFactory

class EventBotClient(BotClient):

    def __init__(self, id, argument_parser=None):
        self._running = False
        self._first_time = True
        self._session_saving_mode = False
        BotClient.__init__(self, id, argument_parser=argument_parser)

    def prior_to_run_loop(self):
        pass

    def run_loop(self):
        #todo change this back to work with console
        #client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        self._running = True
        conversation_file = "/home/rohola/conv_questions.p"

        bot = self.bot_factory.bot("bot")

        # mitsuku = ServiceFactory.get_service("mitsuku")
        # while self._running:
        #     message = input(">>")
        #     response = mitsuku.ask_question(bot.client.client_context, message)
        #     print(response)

        bot.initiate_conversation_storage()


        while self._running:
            if self._first_time:
                try:
                    if self._session_saving_mode:
                        client_context = self.load_client_context(self._configuration.client_configuration.default_userid, conversation_file)
                    else:
                        client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
                except Exception as exp:
                    client_context = self.create_client_context("default_userid")
                finally:
                    self._first_time = False

            client_context.bot.conversations["Console"]._properties = {"session_number": 1, "username": "rohola"}

            self._running = self.wait_and_answer(client_context)

            bot.save_conversation(client_context)



    def initial_question(self, request, username):
        question = "session"+str(request.session_number) + " " + username
        return question


    def dictionary_of_response(self, response, robot):
        answer = ""
        image_filename = ""
        duration = ""
        video_filename = ""
        if robot:

            if robot is not None and "options" in robot and "option" in robot['options']:
                answer = robot['options']['option']


            if robot is not None and "image" in robot and "filename" in robot['image']:
                image_filename = robot['image']['filename']


            if robot is not None and "image" in robot and "duration" in robot["image"]:
                duration = robot["image"]["duration"]


            if robot is not None and "video" in robot and "filename" in robot["video"]:
                video_filename = robot["video"]["filename"]


        return {"conversation":
                    {"question": "",
                     "response": response,
                     "answer": answer
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
        raise NotImplementedError("You must override this and implement the logic wait for a question and send an answer back")

    def post_run_loop(self):
        pass

    def run(self):
        #todo refactor to move this out of here
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        filepath = os.path.join(root, "bots//ryan//config.yaml")
        with open(filepath, encoding="utf-8") as file_reader:
            self._yaml_dict = yaml.load(file_reader)

        worker_running = self._yaml_dict["broker"]["running"]

        if self.arguments.noloop is False:
            YLogger.info(self, "Entering conversation loop...")

            self.prior_to_run_loop()

            if worker_running:
                self.worker_run_loop()
            else:
                self.run_loop()

            self.post_run_loop()

        else:
            YLogger.debug(self, "noloop set to True, exiting...")
