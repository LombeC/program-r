from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils


class TemplateDelayNode(TemplateNode):

    def __init__(self):
        super().__init__()
        self._seconds = None

    def resolve_to_string(self, client_context):
        str = "<delay>"
        str += "<seconds>%s</seconds>" % self._seconds.resolve(client_context)
        str += "</delay>"
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[DELAY] %d" % (len(self._children))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        if 'seconds' in expression.attrib:
            self._seconds = graph.get_word_node(expression.attrib['text'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'seconds':
                self._seconds = self.parse_children_as_word_node(graph, child)

            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

