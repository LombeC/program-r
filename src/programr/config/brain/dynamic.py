from programr.utils.logging.ylogger import YLogger

from programr.config.section import BaseSectionConfigurationData


class BrainDynamicsConfiguration(BaseSectionConfigurationData):

    def __init__(self):
        super().__init__("dynamic")
        self._dynamic_sets = {}
        self._dynamic_maps = {}
        self._dynamic_vars = {}

    @property
    def dynamic_sets(self):
        return self._dynamic_sets

    @property
    def dynamic_maps(self):
        return self._dynamic_maps

    @property
    def dynamic_vars(self):
        return self._dynamic_vars

    def load_config_section(self, configuration_file, configuration, bot_root):
        dynamic_config = configuration_file.get_section("dynamic", configuration)
        if dynamic_config is not None:
            self.load_dynamic_sets(configuration_file, dynamic_config)
            self.load_dynamic_maps(configuration_file, dynamic_config)
            self.load_dynamic_vars(configuration_file, dynamic_config)
        else:
            YLogger.error(self, "Config section [dynamic] missing from Brain, using defaults")

    def load_dynamic_sets(self, configuration_file, dynamic_config):
        sets_config = configuration_file.get_option(dynamic_config, "sets")
        if sets_config is not None:
            for set_key in sets_config.keys():
                dyn_set_class = sets_config[set_key]
                self._dynamic_sets[set_key.upper()] = dyn_set_class

    def load_dynamic_maps(self, configuration_file, dynamic_config):
        maps_config = configuration_file.get_option(dynamic_config, "maps")
        if maps_config is not None:
            for map_name in maps_config.keys():
                dyn_map_class = maps_config[map_name]
                self._dynamic_maps[map_name.upper()] = dyn_map_class

    def load_dynamic_vars(self, configuration_file, dynamic_config):
        vars_config = configuration_file.get_option(dynamic_config, "variables")
        if vars_config is not None:
            for var_name in vars_config.keys():
                dyn_var_class = vars_config[var_name]
                self._dynamic_vars[var_name .upper()] = dyn_var_class

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['sets'] = {}
            data['sets']['numeric'] = 'programr.dynamic.sets.numeric.IsNumeric'
            data['sets']['roman'] = 'programr.dynamic.sets.roman.IsRomanNumeral'

            data['maps'] = {}
            data['maps']['romantodec'] = 'programr.dynamic.maps.roman.MapRomanToDecimal'
            data['maps']['dectoroman'] = 'programr.dynamic.maps.roman.MapDecimalToRoman'

            data['variables'] = {}
            data['variables']['gettime'] = 'programr.dynamic.variables.datetime.GetTime'

        else:
            data['sets'] = {}
            for dyn in self._dynamic_sets:
                self.config_to_yaml(data['sets'], dyn, defaults)

            data['maps'] = {}
            for dyn in self._dynamic_maps:
                self.config_to_yaml(data['maps'], dyn, defaults)

            data['variables'] = {}
            for dyn in self._dynamic_vars:
                self.config_to_yaml(data['variables'], dyn, defaults)
