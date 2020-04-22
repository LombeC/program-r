from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.indexed import TemplateIndexedNode

class TemplateRepeatNode(TemplateIndexedNode):
    def __init__(self):
        TemplateIndexedNode.__init__(self)

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)

        if conversation.has_current_question():
            resolved = conversation._answers[-1].sentences_text()
        else:
            resolved = ""

        YLogger.debug(client_context, "Repeat Node [%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        string = "REPEAT"
        return string

    def to_xml(self, client_context):
        print("TO XML")
        xml = "<repeat />"
        return xml

    #######################################################################################################
    # REPEAT_EXPRESSION ::== <repeat />

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")