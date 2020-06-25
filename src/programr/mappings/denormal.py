from programr.mappings.base import DoubleStringPatternSplitCollection

class DenormalCollection(DoubleStringPatternSplitCollection):

    def __init__(self):
        super().__init__()

    def denormalise(self, normal):
        if self.has_key(normal):
            return self.value(normal)
        return None

    def denormalise_string(self, string):
        return self.replace_by_pattern(string)
