from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData
from programr.config.brain.service import BrainServiceConfiguration


class BrainServicesConfiguration(BaseSectionConfigurationData):
    def __init__(self):
        super().__init__("services")
        self._services = {}

    def exists(self, name):
        return bool(name in self._services)

    def service(self, name):
        if name in self._services:
            return self._services[name]
        return None

    def services(self):
        return self._services.keys()

    def load_config_section(self, configuration_file, configuration, bot_root):
        services = configuration_file.get_section("services", configuration)
        if services is not None:
            service_keys = configuration_file.get_keys(services)

            for name in service_keys:
                service = BrainServiceConfiguration(name)
                service.load_config_section(configuration_file, services, bot_root)
                self._services[name] = service

        else:
            YLogger.warning(self, "Config section [services] missing from Brain, no services loaded")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['REST'] = {}
            data['REST']['classname'] = 'programr.services.rest.GenericRESTService'
            data['REST']['method'] = 'GET'
            data['REST']['host'] = '0.0.0.0'

            data['Pannous'] = {}
            data['Pannous']['classname'] = 'programr.services.pannous.PannousService'
            data['Pannous']['url'] = 'http://weannie.pannous.com/api'

            data['Pandora'] = {}
            data['Pandora']['classname'] = 'programr.services.pandora.PandoraService'
            data['Pandora']['url'] = 'http://www.pandorabots.com/pandora/talk-xml'

            data['Wikipedia'] = {}
            data['Wikipedia']['classname'] = 'programr.services.wikipediaservice.WikipediaService'

            data['OpenWeatherMap'] = {}
            data['OpenWeatherMap']['classname'] = 'programr.services.openweathermap.WeatherService'

            data['DuckDuckGo'] = {}
            data['DuckDuckGo']['classname'] = 'programr.services.duckduckgo.DuckDuckGoService'
            data['DuckDuckGo']['url'] = 'http://api.duckduckgo.com'
