from programr.utils.logging.ylogger import YLogger
from programr.config.section import BaseSectionConfigurationData
import os

class BrainServiceConfiguration(BaseSectionConfigurationData):

    additionals = ['denied_srai']

    def __init__(self, service_name):
        super().__init__(service_name)
        self._classname = None
        self._method = None
        self._host = None
        self._port = None
        self._url = None
        self._username = None
        self._password = None

    @property
    def classname(self):
        return self._classname

    @property
    def method(self):
        return self._method

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def url(self):
        return self._url

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password


    def additionals_to_add(self):
        return BrainServiceConfiguration.additionals

    def load_config_section(self, configuration_file, configuration, bot_root):
        service = configuration_file.get_section(self.section_name, configuration)
        if service is not None:
            self._classname = configuration_file.get_option(service, "classname", missing_value=None)
            self._method = configuration_file.get_option(service, "method", missing_value=None)
            self._host = configuration_file.get_option(service, "host", missing_value=None)
            self._port = configuration_file.get_option(service, "port", missing_value=None)
            self._url = configuration_file.get_option(service, "url", missing_value=None)
            self._username = configuration_file.get_option(service, "username", missing_value=None)
            password_file = configuration_file.get_option(service, "password", missing_value=None)

            if password_file:
                password_file = self.sub_bot_root(password_file, bot_root)
                try:
                    self._password = open(password_file).readline()
                except Exception as e:
                    YLogger.error(self, "couldn't open password file")

            self.load_additional_key_values(configuration_file, service)
        else:
            YLogger.warning(self, "'services' section missing from brain config, using to defaults")

    def to_yaml(self, data, defaults=True):
        data['classname'] = self._classname
        data['method'] = self._method
        data['host'] = self._host
        data['port'] = self._port
        data['url'] = self._url
