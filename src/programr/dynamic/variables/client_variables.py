from programr.dynamic.variables.variable import DynamicVariable


class Name(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        return client_context.bot._conversation_storage.user_name



class Location(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        return client_context.bot._conversation_storage.location


class TimeZone(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        return client_context.bot._conversation_storage.time_zone