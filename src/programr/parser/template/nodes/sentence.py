from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode



class TemplateSentenceNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        result = self.resolve_children_to_string(client_context)
        first = result[:1]
        rest = result[1:]
        resolved = first.upper() + rest.lower()
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "SENTENCE"

    def to_xml(self, client_context):
        xml = "<sentence>"
        xml += self.children_to_xml(client_context)
        xml += "</sentence>"
        return xml

    #######################################################################################################
    # <sentence>ABC</sentence>

    def add_default_star(self):
        return True

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
