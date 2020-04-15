from programr.utils.logging.ylogger import YLogger

from programr.config.base import BaseConfigurationData
from programr.config.bot.redisstorage import BotConversationsRedisStorageConfiguration
from programr.config.bot.filestorage import BotConversationsFileStorageConfiguration
from programr.dialog.storage.factory import ConversationStorageFactory

class BotConversationsConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="conversations")
        self._max_histories = 100
        self._restore_last_topic = False
        self._initial_topic = "*"
        self._type = None
        self._storage = None
        self._empty_on_start = False

    @property
    def max_histories(self):
        return self._max_histories

    @property
    def initial_topic(self):
        return self._initial_topic

    @property
    def restore_last_topic(self):
        return self._restore_last_topic

    @property
    def type(self):
        return self._type

    @property
    def storage(self):
        return self._storage

    @property
    def empty_on_start(self):
        return self._empty_on_start

    def load_config_section(self, configuration_file, configuration, bot_root):
        Conversations = configuration_file.get_section(self._section_name, configuration)
        if Conversations is not None:

            self._max_histories = configuration_file.get_int_option(Conversations, "max_histories", missing_value=100)
            self._initial_topic = configuration_file.get_option(Conversations, "initial_topic", missing_value="*")
            self._restore_last_topic = configuration_file.get_bool_option(Conversations, "restore_last_topic", missing_value=False)

            self._type = configuration_file.get_option(Conversations, "type", missing_value=None)
            config_name = configuration_file.get_option(Conversations, "config_name", missing_value=None)
            self._empty_on_start = configuration_file.get_bool_option(Conversations, "empty_on_start", missing_value=False)

            self._storage = ConversationStorageFactory.get_storage_config(self._type, config_name, configuration_file, configuration, bot_root)
        else:
            YLogger.warning(self, "'Conversations' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['type'] = "file"
            data['max_histories'] = 100
            data['restore_last_topic'] = True
            data['initial_topic'] = "*"
            data['empty_on_start'] = True
        else:
            data['type'] = self._type
            data['max_histories'] = self._max_histories
            data['restore_last_topic'] = self._restore_last_topic
            data['initial_topic'] = self._initial_topic
            data['empty_on_start'] = self._empty_on_start

        self.config_to_yaml(data, BotConversationsFileStorageConfiguration("file"), defaults)
        self.config_to_yaml(data, BotConversationsRedisStorageConfiguration("redis"), defaults)