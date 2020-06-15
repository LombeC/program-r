from programr.dynamic.variables.variable import DynamicVariable


class Name(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        return client_context.get_user_name()
        # return client_context.bot._conversation_storage.user_name


class Location(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        # TODO: Make location a variable of client_context matched by userid
        return client_context.get_location()


class TimeZone(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        return client_context.get_time_zone()
        # return client_context.bot._conversation_storage.time_zone
