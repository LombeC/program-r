from programr.utils.logging.ylogger import YLogger

from programr.config.base import BaseConfigurationData

class BotSessionConfiguration(BaseConfigurationData):


    def __init__(self):
        BaseConfigurationData.__init__(self, name="session")
        self._session_saving_mode = None
        self._session_saving_dir = None


    @property
    def session_saving_mode(self):
        return self._session_saving_mode

    @property
    def session_saving_dir(self):
        return self._session_saving_dir


    def load_config_section(self, configuration_file, configuration, bot_root):
        session_saving = configuration_file.get_section(self._section_name, configuration)
        if session_saving is not None:
            self._session_saving_mode = configuration_file.get_bool_option(session_saving, "session_saving_mode", missing_value=False)
            session_saving_dir = configuration_file.get_option(session_saving, "session_saving_dir", missing_value=".")
            self._session_saving_dir = self.sub_bot_root(session_saving_dir, bot_root)

        else:
            YLogger.warning(self, "'session' section missing from bot config, using defaults")
