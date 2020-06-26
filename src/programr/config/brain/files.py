from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData
from programr.config.brain.aiml_file import BrainAIMLFileConfiguration
from programr.config.brain.file import BrainFileConfiguration


class BrainFilesConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        super().__init__("files")
        self._aiml_files = BrainAIMLFileConfiguration()
        self._set_files = BrainFileConfiguration("sets")
        self._map_files = BrainFileConfiguration("maps")
        self._rdf_files = BrainFileConfiguration("rdf")

        self._denormal = None
        self._normal = None
        self._gender = None
        self._person = None
        self._person2 = None
        self._properties = None
        self._variables = None
        self._triples = None
        self._preprocessors = None
        self._postprocessors = None
        self._regex_templates = None

    @property
    def aiml_files(self):
        return self._aiml_files

    @property
    def set_files(self):
        return self._set_files

    @property
    def map_files(self):
        return self._map_files

    @property
    def denormal(self):
        return self._denormal

    @property
    def normal(self):
        return self._normal

    @property
    def gender(self):
        return self._gender

    @property
    def person(self):
        return self._person

    @property
    def person2(self):
        return self._person2

    @property
    def properties(self):
        return self._properties

    @property
    def variables(self):
        return self._variables

    @property
    def rdf_files(self):
        return self._rdf_files

    @property
    def triples(self):
        return self._triples

    @property
    def preprocessors(self):
        return self._preprocessors

    @property
    def postprocessors(self):
        return self._postprocessors

    @property
    def regex_templates(self):
        return self._regex_templates

    def load_config_section(self, configuration_file, configuration, bot_root):
        files_config = configuration_file.get_section("files", configuration)
        if files_config is not None:
            self._aiml_files.load_config_section(configuration_file, files_config, bot_root)
            self._set_files.load_config_section(configuration_file, files_config, bot_root)
            self._map_files.load_config_section(configuration_file, files_config, bot_root)
            self._rdf_files.load_config_section(configuration_file, files_config, bot_root)

            self._denormal = self._get_file_option(configuration_file, "denormal", files_config, bot_root)
            self._normal = self._get_file_option(configuration_file, "normal", files_config, bot_root)
            self._gender = self._get_file_option(configuration_file, "gender", files_config, bot_root)
            self._person = self._get_file_option(configuration_file, "person", files_config, bot_root)
            self._person2 = self._get_file_option(configuration_file, "person2", files_config, bot_root)
            self._properties = self._get_file_option(configuration_file, "properties", files_config, bot_root)
            self._variables = self._get_file_option(configuration_file, "variables", files_config, bot_root)
            self._triples = self._get_file_option(configuration_file, "triples", files_config, bot_root)
            self._preprocessors = self._get_file_option(configuration_file, "preprocessors", files_config, bot_root)
            self._postprocessors = self._get_file_option(configuration_file, "postprocessors", files_config, bot_root)
            self._regex_templates = self._get_file_option(configuration_file, "regex_templates", files_config, bot_root)
        else:
            YLogger.error(self, "Config section [files] missing from Brain, default values not appropriate")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['denormal'] = "./config/denormal.txt"
            data['normal'] = "./config/normal.txt"
            data['gender'] = "./config/gender.txt"
            data['person'] = "./config/person.txt"
            data['person2'] = "./config/person2.txt"
            data['properties'] = "./config/properties.txt"
            data['variables'] = "./config/variables.txt"
            data['triples'] = "./config/triples.txt"
            data['preprocessors'] = "./config/preprocessors.txt"
            data['postprocessors'] = "./config/postprocessors.txt"
            data['regex_templates'] = "./config/regex.txt"
        else:
            data['denormal'] = self._denormal
            data['normal'] = self._normal
            data['gender'] = self._gender
            data['person'] = self._person
            data['person2'] = self._person2
            data['properties'] = self._properties
            data['variables'] = self._variables
            data['triples'] = self._triples
            data['preprocessors'] = self._preprocessors
            data['postprocessors'] = self._postprocessors
            data['regex_templates'] = self._regex_templates

        self.config_to_yaml(data, BrainAIMLFileConfiguration(), defaults)
        self.config_to_yaml(data, BrainFileConfiguration("sets"), defaults)
        self.config_to_yaml(data, BrainFileConfiguration("maps"), defaults)
        self.config_to_yaml(data, BrainFileConfiguration("rdf"), defaults)

