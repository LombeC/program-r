from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData


class BrainBraintreeConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        super().__init__("braintree")
        self._file = None
        self._content = None

    @property
    def file(self):
        return self._file

    @property
    def content(self):
        return self._content

    def load_config_section(self, configuration_file, configuration, bot_root):
        braintree = configuration_file.get_section("braintree", configuration)
        if braintree is not None:
            file = configuration_file.get_option(braintree, "file", missing_value=None)
            if file is not None:
                self._file = self.sub_bot_root(file, bot_root)
            self._content = configuration_file.get_option(braintree, "content", missing_value="txt")
        else:
            YLogger.warning(self, "'braintree' section missing from bot config, using to defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['file'] = "./braintree.xml"
            data['content'] = "xml"
        else:
            data['file'] = self._file
            data['content'] = self._content
