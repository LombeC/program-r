from programr.mappings.base import DoubleStringCharSplitCollection

class ClientPropertiesCollection(DoubleStringCharSplitCollection):

    def __init__(self):
        DoubleStringCharSplitCollection.__init__(self)

    def get_split_char(self):
        return ":"

    def has_property(self, key):
        return self.has_key(key)

    def property(self, key):
        return self.value(key)

    def add_property(self, key, value):
        key = key.strip()
        value = value.strip()
        if self.has_property(key):
            self.set_value(key, value)
        else:
            self.pairs.append([key, value])

    #TODO: Write load_from_database
    def load_from_database(self):
        pass

