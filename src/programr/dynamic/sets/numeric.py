from programr.dynamic.sets.set import DynamicSet


class IsNumeric(DynamicSet):

    NAME = "NUMBER"

    def __init__(self, config):
        super().__init__(config)

    def is_member(self, client_context, value):
        if value is not None:
            return value.isnumeric()
        return False
