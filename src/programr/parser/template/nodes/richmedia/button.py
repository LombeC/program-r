from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils


class TemplateButtonNode(TemplateNode):

    def __init__(self):
        super().__init__()
        self._text = None
        self._url = None
        self._postback = None

    def resolve_to_string(self, client_context):
        str = "<button>"
        str += "<text>%s</text>" % self._text.resolve(client_context)
        if self._url is not None:
            str += "<url>%s</url>" % self._url.resolve(client_context)
        if self._postback is not None:
            str += "<postback>%s</postback>" % self._postback.resolve(client_context)
        str += "</button>"
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[BUTTON] %d" % (len(self._children))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        if 'text' in expression.attrib:
            self._text = graph.get_word_node(expression.attrib['text'])

        if 'url' in expression.attrib:
            self._url = graph.get_word_node(expression.attrib['url'])

        if 'postback' in expression.attrib:
            self._postback = graph.get_word_node(expression.attrib['postback'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'text':
                self._text = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'url':
                self._url = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'postback':
                self._postback = self.parse_children_as_word_node(graph, child)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

