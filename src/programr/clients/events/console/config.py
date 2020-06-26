from programr.config.client.config import ClientConfigurationData


class ConsoleConfiguration(ClientConfigurationData):

    def __init__(self):
        super().__init__("console")
        self._default_userid = "console"
        self._prompt = ">>>"

    @property
    def default_userid(self):
        return self._default_userid

    @property
    def prompt(self):
        return self._prompt

    def load_configuration(self, configuration_file, bot_root):
        console = configuration_file.get_section(self.section_name)
        if console is not None:
            self._default_userid = configuration_file.get_option(console, "default_userid", missing_value="Console")
            self._prompt = configuration_file.get_option(console, "prompt", missing_value=">>>")
        super().load_configuration(configuration_file, console, bot_root)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['default_userid'] = "console"
            data['prompt'] = ">>>"
        else:
            data['default_userid'] = self._default_userid
            data['prompt'] = self._prompt
        super(ConsoleConfiguration, self).to_yaml(data, defaults)