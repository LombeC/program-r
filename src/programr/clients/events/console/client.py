import re

from programr.utils.logging.ylogger import YLogger
from programr.clients.events.client import EventBotClient
from programr.clients.events.console.config import ConsoleConfiguration


class ConsoleBotClient(EventBotClient):

    def __init__(self, argument_parser=None):
        self.running = False
        EventBotClient.__init__(self, "Console", argument_parser)
        a=1

    def get_description(self):
        return 'ProgramR AIML2.0 Console Client'

    def get_client_configuration(self):
        return ConsoleConfiguration()

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
        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def process_question_with_options(self, client_context, question):
        return client_context.bot.ask_question_with_options(client_context, question, responselogger=self)


    def render_response(self, client_context, response):
        # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        print("\n")
        print(response)
        print("\n")

    def process_question_answer(self, client_context):
        question = self.get_question(client_context)
        response = self.process_question(client_context, question)
        self.render_response(client_context, response)

    def process_question_answer_with_options(self, client_context):
        try:
            YLogger.debug(client_context, "before get_question")
            question = self.get_question(client_context)
            # FIXME: Right now nothing is being done with the options being returned.
            response, options = self.process_question_with_options(client_context, question)

            self.render_response(client_context, response)
        except Exception as ex:
            YLogger.exception(client_context, "Exception caught in process_question_answer_with_options !", ex)

    def wait_and_answer(self, client_context):
        running = True
        try:
            #client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            #self.process_question_answer(client_context)
            self.process_question_answer_with_options(client_context)
        except KeyboardInterrupt as keye:
            running = False
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self._renderer.render(client_context, client_context.bot.get_exit_response(client_context))
        except Exception as excep:
            YLogger.exception(self, "Oops something bad happened !", excep)
        return running

    def prior_to_run_loop(self):
        client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        self.display_startup_messages(client_context)

    def run(self):
        if self.arguments.noloop is False:
            YLogger.info(self, "Entering conversation loop...")

            self.prior_to_run_loop()

            self.run_loop()

            self.post_run_loop()

        else:
            YLogger.debug(self, "noloop set to True, exiting...")


if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = ConsoleBotClient()
        console_app.run()

    run()
