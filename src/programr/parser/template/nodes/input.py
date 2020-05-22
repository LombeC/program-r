from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.indexed import TemplateIndexedNode
from programr.parser.exceptions import ParserException


######################################################################################################################
#
# <input index=”n”/> is replaced with the value of the nth previous sentence input to the bot.
# The input element returns the entire user’s input. This is distinct from the star element,
# which returns only contents captured by a wildcard in the matched pattern.

class TemplateInputNode(TemplateIndexedNode):

    def __init__(self, index=0):
        TemplateIndexedNode.__init__(self, index)

    def get_default_index(self):
        return 0

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)
        question = conversation.current_question()
        if self.index == 0:
            resolved = question.combine_sentences()
        else:
            # resolved = question.previous_nth_sentence(self.index).text()
            resolved = conversation.previous_nth_question(self.index).combine_sentences()
            # print("resolved type: {}".format(type(resolved)))
            # print("resolved: {}".format(resolved))
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    
    # def resolve_to_string(self, client_context):
    #     conversation = client_context.bot.get_conversation(client_context)
    #     int_index = int(self.index.resolve(client_context))
    #     question = conversation.previous_nth_question(int_index)
    #     resolved = question.combine_sentences(client_context)

    #     YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
    #     return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        string = "INPUT"
        string += self.get_index_as_str()
        return string

    def to_xml(self, client_context):
        xml = "<input"
        xml += self.get_index_as_xml()
        xml += ">"
        xml += "</input>"
        return xml

    #######################################################################################################
    # INPUT_EXPRESSION ::== <input( INDEX_ATTRIBUTE)/> | <input><index>TEMPLATE_EXPRESSION</index></input>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")
        if self.children:
            raise ParserException("<input> node should not contain child text, use <input /> or <input></input> only")
