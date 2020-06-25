from programr.utils.logging.ylogger import YLogger
from programr.processors.processing import PostProcessor

DEBUG = False

class DenormalizePostProcessor(PostProcessor):

    def __init__(self):
        super().__init__()

    def process(self, context, word_string):
        denormalized = context.brain.denormals.denormalise_string(word_string)
        if DEBUG: YLogger.debug(context, "Denormalising input from [%s] to [%s]", word_string, denormalized)
        return denormalized
