from programr.utils.logging.ylogger import YLogger

from programr.parser.exceptions import ParserException
from programr.parser.template.nodes.attrib import TemplateAttribNode


######################################################################################################################
#
class TemplateIndexedNode(TemplateAttribNode):

    def __init__(self, index=1):
        super().__init__()
        self._index = index

    def get_default_index(self):
        return 1

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    def get_index_as_str(self):
        string = ""
        if self.index != self.get_default_index():
            string += " index=%d"%self.index
        return string

    def get_index_as_xml(self):
        xml = ""
        if self.index != self.get_default_index():
            xml += ' index="%d"'%self.index
        return xml

    def set_attrib(self, attrib_name, attrib_value):

        if attrib_name != 'index':
            raise ParserException("Invalid attribute name [%s] for this node" % (attrib_name))

        if isinstance(attrib_value, int):
            self._index = attrib_value
        else:
            try:
                self._index = int(attrib_value)
            except:
                raise ParserException("None numeric format [%s] for this node [%s]", attrib_value, attrib_name)

        #if self._index == 0:
        #    raise ParserException("Index values are 1 based, cannot be 0")

######################################################################################################################
#
class TemplateDoubleIndexedNode(TemplateAttribNode):

    def __init__(self, question=1, sentence=1):
        super().__init__()
        self._question = question
        self._sentence = sentence

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question):
        self._question = question

    @property
    def sentence(self):
        return self._sentence

    @sentence.setter
    def sentence(self, sentence):
        self._sentence = sentence

    def get_question_and_sentence_as_str(self):
        string = ""
        if self.question != 1:
            string += " question=%d"%self.question
        if self.sentence != 1:
            if self.sentence == -1:
                string += " sentence=*"
            else:
                string += " sentence=%d"%self.sentence
        return string

    def get_question_and_sentence_as_index_xml(self):
        xml = ""
        if self.question > 1 and self.sentence > 1:
            xml += ' index="%d,%d"'%(self.question, self.sentence)
        elif self.question > 1 and self.sentence == -1:
            xml += ' index="%d,*"'%self.question
        elif self.question == 1 and self.sentence > 1:
            xml += ' index="1,*"'# %self.sentence
        elif self.question > 1 and self.sentence == 1:
            xml += ' index="%d"'%self.question
        return xml

    def set_attrib(self, attrib_name, attrib_value):

        if attrib_name != 'index':
            raise ParserException("Invalid attribute name [%s] for this node" % (attrib_name))

        if isinstance(attrib_value, int):
            int_val = attrib_value
            self._sentence = int_val
        else:
            splits = attrib_value.split(",")
            if len(splits) == 1:
                try:
                    self._sentence = int(splits[0])
                except Exception as excep:
                    YLogger.exception(self, "Failed to split string", excep)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x' or 'x,y'",
                                          attrib_value, attrib_name)
            elif len(splits) == 2:
                try:
                    self._question = int(splits[0])
                    if splits[1] == '*':
                        self._sentence = -1
                    else:
                        self._sentence = int(splits[1])
                except Exception as excep:
                    YLogger.exception(self, "Failed to split string", excep)
                    raise ParserException("None numeric format [%s] for this node [%s], either 'x', 'x,y', or 'x,*'",
                                          attrib_value, attrib_name)

        if self._sentence == 0:
            raise ParserException("Sentence values are 1 based, cannot be 0")

        if self._question == 0:
            raise ParserException("Question values are 1 based, cannot be 0")
