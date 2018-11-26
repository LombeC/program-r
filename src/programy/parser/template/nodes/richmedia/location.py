from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException


class TemplateLocationNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        str = "<location />"
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[LOCATION]"

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #
    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)

