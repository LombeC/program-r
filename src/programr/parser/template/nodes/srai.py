from programr.utils.logging.ylogger import YLogger
# from programr.bot import Bot
from programr.parser.template.nodes.base import TemplateNode


class TemplateSRAINode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        srai_text = self.resolve_children_to_string(client_context)
        YLogger.debug(client_context, "[%s] SRAI Text [%s]", self.to_string(), srai_text)

        resolved = client_context.bot.ask_question(client_context, srai_text, srai=True)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[SRAI]"

    def to_xml(self, client_context):
        xml = "<srai>"
        xml += self.children_to_xml(client_context)
        xml += "</srai>"
        return xml

    #######################################################################################################
    # SRAI_EXPRESSION ::== <srai>TEMPLATE_EXPRESSION</srai>

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
