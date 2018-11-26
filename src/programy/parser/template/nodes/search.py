from programy.utils.logging.ylogger import YLogger
from urllib.parse import urlencode

from programy.parser.template.nodes.base import TemplateNode


class TemplateSearchNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        string = self.resolve_children_to_string(client_context)
        query = {'q': string}
        encoded = urlencode(query)
        resolved = "https://www.google.co.uk/search?" + encoded
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "SEARCH"

    def to_xml(self, client_context):
        xml = "<search>"
        xml += self.children_to_xml(client_context)
        xml += "</search>"
        return xml

    #######################################################################################################
    # SEARCH_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def add_default_star(self):
        return True

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
