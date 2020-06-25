from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.template.nodes.richmedia.button import TemplateButtonNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils


class TemplateCardNode(TemplateNode):

    def __init__(self):
        super().__init__()
        self._image = None
        self._title = None
        self._subtitle = None
        self._buttons = []

    def resolve_to_string(self, client_context):
        str = "<card>"
        str += "<image>%s</image>" % self._image.resolve(client_context)
        str += "<title>%s</title>" % self._title.resolve(client_context)
        str += "<subtitle>%s</subtitle>" % self._subtitle.resolve(client_context)
        for button in self._buttons:
            str += button.resolve_to_string(client_context)
        str += "</card>"
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[CARD] %d" % (len(self._buttons))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        if 'image' in expression.attrib:
            self._image = graph.get_word_node(expression.attrib['image'])

        if 'title' in expression.attrib:
            self._title = graph.get_word_node(expression.attrib['title'])

        if 'subtitle' in expression.attrib:
            self._subtitle = graph.get_word_node(expression.attrib['subtitle'])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'image':
                self._image = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'title':
                self._title = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'subtitle':
                self._subtitle = self.parse_children_as_word_node(graph, child)
            elif tag_name == 'button':
                button_class = graph.get_node_class_by_name("button")
                button = button_class()
                button.parse_expression(graph, child)
                self._buttons.append(button)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

