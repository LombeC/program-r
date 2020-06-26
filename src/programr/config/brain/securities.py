from programr.config.section import BaseSectionConfigurationData
from programr.config.brain.security import BrainSecurityAuthenticationConfiguration
from programr.config.brain.security import BrainSecurityAuthorisationConfiguration



class BrainSecuritiesConfiguration(BaseSectionConfigurationData):
    def __init__(self):
        super().__init__("security")
        self._authorisation = None
        self._authentication = None

    @property
    def authorisation(self):
        return self._authorisation

    @property
    def authentication(self):
        return self._authentication

    def load_config_section(self, configuration_file, configuration, bot_root):
        securities = configuration_file.get_section(self.section_name, configuration)
        if securities is not None:
            self._authentication = BrainSecurityAuthenticationConfiguration()
            self._authentication.load_config_section(configuration_file, securities, bot_root)

            self._authorisation = BrainSecurityAuthorisationConfiguration()
            self._authorisation.load_config_section(configuration_file, securities, bot_root)

    def to_yaml(self, data, defaults=True):
        self.config_to_yaml(data, BrainSecurityAuthenticationConfiguration(), defaults)
        self.config_to_yaml(data, BrainSecurityAuthorisationConfiguration(), defaults)
