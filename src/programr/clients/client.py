import os
import logging.config
import yaml
import pickle

from programr.utils.logging.ylogger import YLogger

from programr.config.file.factory import ConfigurationFactory
from programr.clients.args import CommandLineClientArguments
from programr.bot import Bot
from programr.config.programr import ProgramrConfiguration
from programr.context import ClientContext
from programr.utils.license.keys import LicenseKeys
from programr.utils.classes.loader import ClassLoader
from programr.scheduling.scheduler import ProgramrScheduler
from programr.clients.render.text import TextRenderer
from programr.utils.classes.loader import ClassLoader


class ResponseLogger(object):

    def log_unknown_response(self, question):
        return

    def log_response(self, question, answer):
        return


class BotSelector(object):

    def __init__(self, configuration):
        self._configuration = configuration

    def select_bot(self, bots):
        pass


class DefaultBotSelector(BotSelector):

    def __init__(self, configuration):
        BotSelector.__init__(self, configuration)

    def select_bot(self, bots):
        if bots:
            return next(iter(bots.values()))
        return None


class BotFactory(object):

    def __init__(self, client, configuration):
        self._client = client
        self._bots = {}
        self.load_bots(configuration)
        self._bot_selector = None
        self.load_bot_selector(configuration)

    def botids(self):
        return self._bots.keys()

    def bot(self, id):
        if id in self._bots:
            return self._bots[id]
        else:
            return None

    def load_bots(self, configuration):
        for config in configuration.configurations:
            bot = Bot(config, client=self._client)
            self._bots[bot.id] = bot

    def load_bot_selector(self, configuration):
        if configuration.bot_selector is None:
            self._bot_selector = DefaultBotSelector(configuration)
        else:
            try:
                self._bot_selector = ClassLoader.instantiate_class(configuration.bot_selector)(configuration)
            except Exception as e:
                self._bot_selector = DefaultBotSelector(configuration)

    def select_bot(self):
        return self._bot_selector.select_bot(self._bots)


class BotClient(ResponseLogger):

    def __init__(self, id, argument_parser=None):
        self._id = id

        self._arguments = self.parse_arguments(argument_parser=argument_parser)
        # print("self._arguments: {}".format(self._arguments))
        self.initiate_logging(self.arguments)

        self._configuration = None
        self.load_configuration(self.arguments)
        self.parse_configuration()

        self._bot_factory = BotFactory(self, self.configuration.client_configuration)

        self._license_keys = LicenseKeys()
        self.load_license_keys()
        self.get_license_keys()

        self._scheduler = None
        self.load_scheduler()

        self._renderer = self.load_renderer()

    def ylogger_type(self):
        return "client"

    @property
    def configuration(self):
        return self._configuration

    @property
    def id(self):
        return self._id

    @property
    def arguments(self):
        return self._arguments

    @property
    def license_keys(self):
        return self._license_keys

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def bot_factory(self):
        return self._bot_factory

    @property
    def renderer(self):
        return self._renderer

    @property
    def session_saving_mode(self):
        return self._session_saving_mode


    @property
    def client_context(self):
        session_pickle_dir= self.configuration.client_configuration.configurations[0].session.session_saving_dir
        self._session_saving_mode = self.configuration.client_configuration.configurations[0].session.session_saving_mode
        if self.session_saving_mode:
            try:
                client_context = self.load_client_context(
                    self.configuration.client_configuration.default_userid, session_pickle_dir)
            except Exception as exp:
                YLogger.exception(self, "could not load the session pickles", exp)
                client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        else:
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        return client_context

    def get_description(self):
        raise NotImplementedError("You must override this and return a client description")

    def add_client_arguments(self, parser=None):
        # Nothing to add
        return

    def parse_configuration(self):
        # Nothing to add
        return

    def parse_args(self, arguments, parsed_args):
        # Nothing to add
        return

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=argument_parser)
        client_args.parse_args(self)
        return client_args

    def load_license_keys(self):
        if self.configuration is not None:
            if self.configuration.client_configuration.license_keys is not None:
                YLogger.debug(self, f"filename containing license keys: {self.configuration.client_configuration.license_keys}")
                self._license_keys.load_license_key_file(self.configuration.client_configuration.license_keys)
            else:
                YLogger.warning(self, "No client configuration setting for license_keys")
        else:
            YLogger.warning(self, "No configuration defined when loading license keys")

    def get_license_keys(self):
        return

    def initiate_logging(self, arguments):
        if arguments.logging is not None:
            with open(arguments.logging, 'r+', encoding="utf-8") as yml_data_file:
                logging_config = yaml.load(yml_data_file, Loader=yaml.FullLoader)
                logging.config.dictConfig(logging_config)
                YLogger.info(self, "Now logging under configuration")
        else:
            print("Warning. No logging configuration file defined, using defaults...")

    def get_client_configuration(self):
        """
        By overriding this class in you Configuration file, you can add new configurations
        and stil use the dynamic loader capabilities
        :return: Client configuration object
        """
        raise NotImplementedError("You must override this and return a subclassed client configuration")

    def load_configuration(self, arguments):
        if arguments.bot_root is None:
            if arguments.config_filename is not None:
                arguments.bot_root = os.path.dirname(arguments.config_filename)
            else:
                arguments.bot_root = "."
            print("No bot root argument set, defaulting to [%s]" % arguments.bot_root)

        if arguments.config_filename is not None:
            self._configuration = ConfigurationFactory.load_configuration_from_file(self.get_client_configuration(),
                                                                                    arguments.config_filename,
                                                                                    arguments.config_format,
                                                                                    arguments.bot_root)
        else:
            print("No configuration file specified, using defaults only !")
            self._configuration = ProgramrConfiguration(self.get_client_configuration())

    def load_scheduler(self):
        if self.configuration.client_configuration.scheduler is not None:
            self._scheduler = ProgramrScheduler(self, self.configuration.client_configuration.scheduler)
            self._scheduler.start()

    def create_client_context(self, userid, load_variables=True):
        client_context = ClientContext(self, userid)
        client_context.bot = self._bot_factory.select_bot()
        #TODO: here is where we need to load in variables
        client_context.brain = client_context.bot._brain_factory.select_brain()
        if load_variables: client_context.brain._load_variables(client_context)
        return client_context

    def load_client_context(self, userid, session_pickle_dir):
        questions_save_file = os.path.join(session_pickle_dir, "questions.p")
        properties_save_file = os.path.join(session_pickle_dir, "properties.p")
        questions_pickle_file = open(questions_save_file, 'rb')
        properties_pickle_file = open(properties_save_file, 'rb')
        questions = pickle.load(questions_pickle_file)
        properties = pickle.load(properties_pickle_file)
        client_context = self.create_client_context(userid)
        client_context.brain.bot.set_conversation_question(client_context, questions)
        client_context.bot.conversations[userid].set_properties(properties)
        return client_context

    def load_renderer(self):
        try:
            if self.get_client_configuration().renderer is not None:
                clazz = ClassLoader.instantiate_class(self.get_client_configuration().renderer.renderer)
                return clazz(self)
        except Exception as e:
            YLogger.exception(None, "Failed to load config specified renderer", e)

        return self.get_default_renderer()

    def get_default_renderer(self):
        return TextRenderer(self)

    def get_question(self, client_context):
        raise NotImplementedError("You must override this and implement the logic")

    def process_question(self, client_context, question):
        raise NotImplementedError("You must override this and implement the logic to create a response to the question")

    def render_response(self, client_context, response):
        raise NotImplementedError(
            "You must override this and implement the logic to process the response by rendering using a RCS renderer")

    def process_response(self, client_context, response):
        raise NotImplementedError("You must override this and implement the logic to display the response to the user")

    def run(self):
        raise NotImplementedError("You must override this and implement the logic to run the client")
