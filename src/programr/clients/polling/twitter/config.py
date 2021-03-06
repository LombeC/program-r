from programr.config.client.config import ClientConfigurationData


class TwitterConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "twitter")
        self._polling_interval = 0
        self._rate_limit_sleep = -1
        self._use_status = False
        self._use_direct_message = False
        self._auto_follow = False
        self._storage = None
        self._storage_location = None
        self._welcome_message = "Thanks for following me."

    @property
    def polling_interval(self):
        return self._polling_interval

    @property
    def rate_limit_sleep(self):
        return self._rate_limit_sleep

    @property
    def use_status(self):
        return self._use_status

    @property
    def use_direct_message(self):
        return self._use_direct_message

    @property
    def auto_follow(self):
        return self._auto_follow

    @property
    def storage(self):
        return self._storage

    @property
    def storage_location(self):
        return self._storage_location

    @property
    def welcome_message(self):
        return self._welcome_message

    def load_configuration(self, configuration_file, bot_root):
        twitter = configuration_file.get_section(self.section_name)
        if twitter is not None:
            self._polling_interval = configuration_file.get_int_option(twitter, "polling_interval")
            self._rate_limit_sleep = configuration_file.get_int_option(twitter, "rate_limit_sleep", missing_value=-1)
            self._streaming = configuration_file.get_bool_option(twitter, "streaming")
            self._use_status = configuration_file.get_bool_option(twitter, "use_status")
            self._use_direct_message = configuration_file.get_bool_option(twitter, "use_direct_message")
            if self._use_direct_message is True:
                self._auto_follow = configuration_file.get_bool_option(twitter, "auto_follow")

            self._storage = configuration_file.get_option(twitter, "storage")
            if self._storage == 'file':
                storage_loc = configuration_file.get_option(twitter, "storage_location")
                self._storage_location = self.sub_bot_root(storage_loc, bot_root)

            self._welcome_message = configuration_file.get_option(twitter, "welcome_message")
        super(TwitterConfiguration, self).load_configuration(configuration_file, twitter, bot_root)

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['polling_interval'] = 0
            data['rate_limit_sleep'] = -1
            data['use_status'] = False
            data['use_direct_message'] = False
            data['auto_follow'] = False
            data['storage'] = 'file'
            data['storage_location'] = './storage/twitter.data'
            data['welcome_message'] = "Thanks for following me."
        else:
            data['polling_interval'] = self._polling_interval
            data['rate_limit_sleep'] = self._rate_limit_sleep
            data['use_status'] = self._use_status
            data['use_direct_message'] = self._use_direct_message
            data['auto_follow'] = self._auto_follow
            data['storage'] = self._storage
            data['storage_location'] = self._storage_location
            data['welcome_message'] = self._welcome_message

        super(TwitterConfiguration, self).to_yaml(data, defaults)