from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils


class TemplateListNode(TemplateNode):

    def __init__(self):
        super().__init__()
        self._items = []

    def resolve_list_items(self, client_context):
        str = ""
        for item in self._items:
            str += "<item>%s</item>"%item.resolve(client_context)
        return str

    def resolve_to_string(self, client_context):
        str = "<list>"
        str += self.resolve_list_items(client_context)
        str += "</list>"
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[LIST] %d" % (len(self._items))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'item':
                item = self.parse_children_as_word_node(graph, child)
                self._items.append(item)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

