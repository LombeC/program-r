from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils


class TemplateImageNode(TemplateNode):

    def __init__(self):
        super().__init__()

    def resolve_to_string(self, client_context):
        str = "<image>%s</image>"%self.resolve_children_to_string(client_context)
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[IMAGE] %d" % (len(self._children))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #
    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)

