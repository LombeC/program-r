from programr.config.container import BaseContainerConfigurationData
from programr.config.brain.overrides import BrainOverridesConfiguration
from programr.config.brain.defaults import BrainDefaultsConfiguration
from programr.config.brain.nodes import BrainNodesConfiguration
from programr.config.brain.binaries import BrainBinariesConfiguration
from programr.config.brain.braintree import BrainBraintreeConfiguration
from programr.config.brain.files import BrainFilesConfiguration
from programr.config.brain.services import BrainServicesConfiguration
from programr.config.brain.securities import BrainSecuritiesConfiguration
from programr.config.brain.oobs import BrainOOBSConfiguration
from programr.config.brain.dynamic import BrainDynamicsConfiguration
from programr.config.brain.nlp import BrainTokenizerConfiguration
from programr.config.brain.nlp import BrainNLPConfiguration


class BrainConfiguration(BaseContainerConfigurationData):

    def __init__(self, section_name="brain"):
        self._overrides = BrainOverridesConfiguration()
        self._defaults = BrainDefaultsConfiguration()
        self._nodes = BrainNodesConfiguration()
        self._binaries = BrainBinariesConfiguration()
        self._braintree = BrainBraintreeConfiguration()
        self._files = BrainFilesConfiguration()
        self._services = BrainServicesConfiguration()
        self._security = BrainSecuritiesConfiguration()
        self._oob = BrainOOBSConfiguration()
        self._dynamics = BrainDynamicsConfiguration()
        self._tokenizer = BrainTokenizerConfiguration()
        self._nlp = BrainNLPConfiguration()
        super().__init__(section_name)

    @property
    def overrides(self):
        return self._overrides

    @property
    def defaults(self):
        return self._defaults

    @property
    def nodes(self):
        return self._nodes

    @property
    def binaries(self):
        return self._binaries

    @property
    def braintree(self):
        return self._braintree

    @property
    def files(self):
        return self._files

    @property
    def services(self):
        return self._services

    @property
    def security(self):
        return self._security

    @property
    def oob(self):
        return self._oob

    @property
    def dynamics(self):
        return self._dynamics

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def nlp(self):
        return self._nlp

    def load_configuration(self, configuration_file, bot_root):
        brain_config = configuration_file.get_section(self.section_name)
        if brain_config is not None:
            self._overrides.load_config_section(configuration_file, brain_config, bot_root)
            self._defaults.load_config_section(configuration_file, brain_config, bot_root)
            self._nodes.load_config_section(configuration_file, brain_config, bot_root)
            self._binaries.load_config_section(configuration_file, brain_config, bot_root)
            self._braintree.load_config_section(configuration_file, brain_config, bot_root)
            self._files.load_config_section(configuration_file, brain_config, bot_root)
            self._services.load_config_section(configuration_file, brain_config, bot_root)
            self._security.load_config_section(configuration_file, brain_config, bot_root)
            self._oob.load_config_section(configuration_file, brain_config, bot_root)
            self._dynamics.load_config_section(configuration_file, brain_config, bot_root)
            self._tokenizer.load_config_section(configuration_file, brain_config, bot_root)
            self._nlp.load_config_section(configuration_file, brain_config, bot_root)

    def to_yaml(self, data, defaults=True):
        self.config_to_yaml(data, BrainOverridesConfiguration(), defaults)
        self.config_to_yaml(data, BrainDefaultsConfiguration(), defaults)
        self.config_to_yaml(data, BrainNodesConfiguration(), defaults)
        self.config_to_yaml(data, BrainBinariesConfiguration(), defaults)
        self.config_to_yaml(data, BrainBraintreeConfiguration(), defaults)
        self.config_to_yaml(data, BrainFilesConfiguration(), defaults)
        self.config_to_yaml(data, BrainServicesConfiguration(), defaults)
        self.config_to_yaml(data, BrainSecuritiesConfiguration(), defaults)
        self.config_to_yaml(data, BrainOOBSConfiguration(), defaults)
        self.config_to_yaml(data, BrainDynamicsConfiguration(), defaults)
        self.config_to_yaml(data, BrainTokenizerConfiguration(), defaults)
        self.config_to_yaml(data, BrainNLPConfiguration(), defaults)
