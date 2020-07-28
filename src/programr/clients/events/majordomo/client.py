from programr.clients.events.client import EventBotClient
from programr.clients.events.majordomo.config import MajorDomoConfiguration
from programr.majordomo.mdwrkapi import MajorDomoWorker
from programr.majordomo.request import ReadyRequest, UserRequest, SessionRequest, QuestionRequest, ServiceRequest, \
    SessionUserRequest
from programr.utils.logging.ylogger import YLogger
from programr.services.service import ServiceFactory


class MajorDomoBotClient(EventBotClient):

    def __init__(self, argument_parser=None):
        self.running = False
        self.service = None
        super().__init__("majordomo", argument_parser)

    def get_description(self):
        return 'ProgramR AIML2.0 MajorDomo Client'

    def get_client_configuration(self):
        return MajorDomoConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def get_question(self, client_context, input_func=input):
        ask = "%s " % self.get_client_configuration().prompt
        return input_func(ask)

    def display_startup_messages(self, client_context):
        self.process_response(client_context, client_context.bot.get_version_string(client_context))
        initial_question = client_context.bot.get_initial_question(client_context)
        self._renderer.render(client_context, initial_question)

    def process_question(self, client_context, question):
        # Returns a response
        return client_context.bot.ask_question(client_context, question, responselogger=self)

    def process_question_service(self, client_context, question):
        return self.service.ask_question(client_context, question)

    def process_question_with_options(self, client_context, question):
        return client_context.bot.ask_question_with_options(client_context, question, responselogger=self)

    def process_question_answer_with_options(self, client_context):
        question = self.get_question(client_context)
        response = self.process_question_with_options(client_context, question)
        self.render_response(client_context, response)

    def render_response(self, client_context, response):
        response_dict = {}
        response_dict = self.dictionary_of_response(client_context, response)
        response_string = str(response_dict)
        return [response_string]


    def process_response(self, client_context, response):
        print(response)

    def process_question_answer(self, client_context):
        question = self.get_question(client_context)
        response = self.process_question(client_context, question)
        self.render_response(client_context, response)

    def wait_and_answer(self, client_context):
        running = True
        try:
            # client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self.process_question_answer(client_context)
        except KeyboardInterrupt as keye:
            running = False
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self._renderer.render(client_context, client_context.bot.get_exit_response(client_context))
        except Exception as excep:
            YLogger.exception(self, "Oops something bad happened !", excep)
        return running

    def prior_to_run_loop(self):
        userid = "majordomo"
        client_context = self.create_client_context(userid)
        self.display_startup_messages(client_context)

    def worker_run_loop(self):
        majordomo_worker = MajorDomoWorker(self.configuration.client_configuration)
        response = None
        username = None
        client_context = None

        while True:
            print(response)
            request = majordomo_worker.receive(response)
            if request is None:
                YLogger.debug(self, "worker was interrupted")
                break

            if type(request) is ReadyRequest:
                YLogger.info(self, "ready request")
                response = [request.command]

            elif type(request) is UserRequest:
                YLogger.info(self, "user request")
                username = request.username
                client_context = self.client_context
                client_context.bot.initiate_conversation_storage()

            elif type(request) is SessionRequest:
                YLogger.info(self, "session request")
                if client_context is None:
                    YLogger.debug(self, "Client context is not initiated. Messages are out of order")
                    client_context = self.client_context
                    client_context.bot.initiate_conversation_storage()

                if username is not None:
                    question = self.initial_question(request, username)
                    print("question", question)


                    answer = self.process_question_with_options(client_context, question)


                    print("answer", answer)
                    response = self.render_response(client_context, answer)
                else:
                    response = ["username is not specified"]

            elif type(request) is QuestionRequest:
                try:
                    YLogger.info(self, "question request")
                    if client_context is not None:
                        print(request.question)
                        #answer = self.process_question(client_context, request.question)

                        answer = self.process_question_with_options(client_context, request.question)

                        client_context.bot.save_conversation(client_context)
                        response = self.render_response(client_context, answer)
                    else:
                        response = ["client context is not initiated. Initial Session request"]

                except Exception as e:
                    YLogger.exception(self, "chatbot encountered an internal crash", e)


    def worker_run_loop1(self):
        majordomo_worker = MajorDomoWorker(self.configuration.client_configuration)
        response = None
        client_context = None

        print("before while")
        while True:
            print(str(response))
            request = majordomo_worker.receive(response)
            if request is None:
                YLogger.debug(self, "worker was interrupted")
                break

            if type(request) is ReadyRequest:
                YLogger.info(self, "ready request")

                # if the robot sends the ready message again
                # it will NOT reload anything.
                # we can change this part to use it as a signal
                # to initialize client_context
                client_context = self.client_context #MAYBE initialize client context??!

                client_context.bot.initiate_conversation_storage()
                response = [request.command]

            # elif type(request) is ServiceRequest:
            #     self.service = ServiceFactory.get_service(request.service_name)
            elif type(request) is SessionUserRequest:
                YLogger.info(self, "session user request")

                if client_context:
                    session_number = request.session_number
                    username = request.username

                    if self.session_saving_mode:
                        #response = ["welcome to session saving mode"]#todo should pull the latest question we asked
                        last_question = client_context.bot.conversations[self.configuration.client_configuration.id].questions[-1].sentences[-1].response
                        response = self.render_response(client_context, last_question)

                    else:
                        question = self.initial_question(request, request.username)
                        print("question", question)

                        answer = self.process_question_with_options(client_context, question)
                        print("answer", answer)
                        response = self.render_response(client_context, answer)
                else:

                    response = ["client context is not initiated. Initial Session request"]



            elif type(request) is QuestionRequest:
                try:
                    YLogger.info(self, "question request")
                    if client_context is not None:
                        print(request.question)

                        # if self._first_time:
                        #     client_context = self.client_context
                        #     self._first_time = False


                        userid = client_context.userid
                        client_context.bot.conversations[userid].set_property("session_number", session_number)
                        client_context.bot.conversations[userid].set_property("username", username)

                        client_context.bot.facial_expression_recognition.append(request.emotion)

                        #answer = self.process_question_service(client_context, request.question)

                        # todo this part should be cleaned up preprocessing question string
                        # import string
                        # exclude = set(string.punctuation)
                        # question_no_punctuation = ''.join(ch for ch in request.question if ch not in exclude)


                        answer = self.process_question_with_options(client_context, request.question)

                        client_context.bot.save_conversation(client_context)
                        response = self.render_response(client_context, answer)
                    else:
                        response = ["client context is not initiated. Initial Session request"]

                except Exception as e:
                    YLogger.exception(self, "chatbot encounter an internal crash", e)

    def worker_run_loop2(self):
        '''
        This loop is for the case that we don't have session and user info
        :return:
        '''
        majordomo_worker = MajorDomoWorker(self.configuration.client_configuration)
        response = None
        client_context = None

        session_number = None
        username = None

        print("before while")
        while True:
            print(str(response))
            request = majordomo_worker.receive(response)
            if request is None:
                YLogger.debug(self, "worker was interrupted")
                break

            if type(request) is ReadyRequest:
                YLogger.info(self, "ready request")

                # if the robot sends the ready message again
                # it will NOT reload anything.
                # we can change this part to use it as a signal
                # to initialize client_context
                client_context = self.client_context #MAYBE initialize client context??!

                client_context.bot.initiate_conversation_storage()
                response = [request.command]


            elif type(request) is QuestionRequest:
                try:
                    YLogger.info(self, "question request")
                    if client_context is not None:
                        print(request.question)

                        # if self._first_time:
                        #     client_context = self.client_context
                        #     self._first_time = False


                        userid = client_context.userid
                        if session_number is None:
                            session_number = 1
                        if username is None:
                            username = "test"

                        client_context.bot.conversations[userid].set_property("session_number", session_number)
                        client_context.bot.conversations[userid].set_property("username", username)

                        client_context.bot.facial_expression_recognition.append(request.emotion)

                        answer = self.process_question_with_options(client_context, request.question)

                        #client_context.bot.save_conversation(client_context)
                        response = self.render_response(client_context, answer)
                    else:
                        response = ["client context is not initiated. Initial Session request"]

                except Exception as e:
                    YLogger.exception(self, "chatbot encounter an internal crash", e)


    def run(self):
        if self.arguments.noloop is False:
            YLogger.info(self, "Entering conversation loop...")

            self.prior_to_run_loop()

            self.worker_run_loop2()

            self.post_run_loop()

        else:
            YLogger.debug(self, "noloop set to True, exiting...")




if __name__ == '__main__':
    def run():
        print("Loading, please wait...")
        majordomo_app = MajorDomoBotClient()
        majordomo_app.run()


    run()


