import os

from programr.clients.events.console.client import ConsoleBotClient
from programr.utils.text.dateformat import DateFormatter

class ProgramRChatbot(ConsoleBotClient):

    def __init__(self, argument_parser=None):
        ConsoleBotClient.__init__(self, argument_parser)

    def parse_configuration(self):
        self.configuration.client_configuration.brain_config[0].brain_config[0].files.aiml_files._files = \
            [os.path.dirname(__file__)]

    def add_local_properties(self):
        client_context = self.create_client_context("console")
        client_context.brain.properties.add_property("name", "ProgramR")
        client_context.brain.properties.add_property("app_version", "1.0.0")
        client_context.brain.properties.add_property("grammar_version", "1.0.0")
        date_formatter = DateFormatter()
        client_context.brain.properties.add_property("birthdate", date_formatter.locate_appropriate_date_time())

if __name__ == '__main__':

    print ("Running ProgramR Chatbot with default options....")

    chatbot = ProgramRChatbot()

    chatbot.add_local_properties()

    chatbot.run()


