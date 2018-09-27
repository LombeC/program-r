
from programy.utils.logging.ylogger import YLogger

from programy.config.section import BaseSectionConfigurationData
from programy.config.brain.oob import BrainOOBConfiguration


class BrainOOBSConfiguration(BaseSectionConfigurationData):
    def __init__(self):
        BaseSectionConfigurationData.__init__(self, "oob")
        self._default = None
        self._oobs = {}

    def exists(self, name):
        if name == 'default':
            return bool(self._default is not None)
        return bool(name in self._oobs)

    def default(self):
        return self._default

    def oob(self, name):
        if name in self._oobs:
            return self._oobs[name]
        return None

    def oobs(self):
        return self._oobs.keys()

    def load_config_section(self, configuration_file, configuration, bot_root):
        oobs = configuration_file.get_section("oob", configuration)
        if oobs is not None:
            oob_keys = configuration_file.get_keys(oobs)

            for name in oob_keys:
                oob = BrainOOBConfiguration(name)
                oob.load_config_section(configuration_file, oobs, bot_root)
                if name == 'default':
                    self._default = oob
                else:
                    self._oobs[name] = oob

        else:
            YLogger.warning(self, "Config section [oobs] missing from Brain, no oobs loaded")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['default'] = {'classname': 'programy.oob.default.DefaultOutOfBandProcessor'}
            data['alarm'] = {'classname': 'programy.oob.alarm.AlarmOutOfBandProcessor'}
            data['camera'] = {'classname': 'programy.oob.camera.CameraOutOfBandProcessor'}
            data['clear'] = {'classname': 'programy.oob.clear.ClearOutOfBandProcessor'}
            data['dial'] = {'classname': 'programy.oob.dial.DialOutOfBandProcessor'}
            data['dialog'] = {'classname': 'programy.oob.dialog.DialogOutOfBandProcessor'}
            data['email'] = {'classname': 'programy.oob.email.EmailOutOfBandProcessor'}
            data['geomap'] = {'classname': 'programy.oob.map.MapOutOfBandProcessor'}
            data['schedule'] = {'classname': 'programy.oob.schedule.ScheduleOutOfBandProcessor'}
            data['search'] = {'classname': 'programy.oob.search.SearchOutOfBandProcessor'}
            data['sms'] = {'classname': 'programy.oob.sms.SMSOutOfBandProcessor'}
            data['url'] = {'classname': 'programy.oob.url.URLOutOfBandProcessor'}
            data['wifi'] = {'classname': 'programy.oob.wifi.WifiOutOfBandProcessor'}
        else:
            if self._default is not None:
                self.config_to_yaml(data, self._default, defaults)
            for oob in self._oobs:
                self.config_to_yaml(data, oob, defaults)
