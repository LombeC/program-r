from programr.utils.logging.ylogger import YLogger
from abc import ABCMeta, abstractmethod

from programr.utils.classes.loader import ClassLoader

class ProcessorLoader(ClassLoader):

    def __init__(self):
        super().__init__()
        self.processors = []

    def empty(self):
        self.processors.clear()

    def load(self, filename, *args, **kw):
        YLogger.debug(self, "Loading processors from file [%s]", filename)
        count = 0
        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line:
                        if line[0] != '#':
                            new_class = ClassLoader.instantiate_class(line)
                            if new_class is not None:
                                self.processors.append(new_class(*args, **kw))
                                count += 1
        except FileNotFoundError:
            YLogger.error(self, "File not found [%s]", filename)
        return count

    def process(self, client_context, string):
        for processor in self.processors:
            string = processor.process(client_context, string)
        return string


##################################################################
#
class Processor:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def process(self, client_context, word_string):
        pass


##################################################################
#
class PreProcessor(Processor):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def process(self, client_context, word_string):
        pass

##################################################################
#
class PostProcessor(Processor):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def process(self, client_context, word_string):
        pass
