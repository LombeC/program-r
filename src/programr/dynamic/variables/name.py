from programr.dynamic.variables.variable import DynamicVariable


class Name(DynamicVariable):

    def __init__(self, config):
        DynamicVariable.__init__(self, config)

    def get_value(self, client_context, value=None):
        # TODO: Need to find a way to pull info from DB
        return client_context.bot._conversation_storage.user_name