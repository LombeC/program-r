from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode


class TemplateUppercaseNode(TemplateNode):

    def __init__(self):
        super().__init__()

    def resolve_to_string(self, client_context):
        resolved = self.resolve_children_to_string(client_context)
        resolved = resolved.upper()
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            data = self.resolve_to_string(client_context)
            return data
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "UPPERCASE"

    def to_xml(self, client_context):
        xml = "<uppercase>"
        xml += self.children_to_xml(client_context)
        xml += "</uppercase>"
        return xml

    #######################################################################################################
    # <uppercase>ABC</uppercase>

    def add_default_star(self):
        return True

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
