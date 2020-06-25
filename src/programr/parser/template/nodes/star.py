from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.indexed import TemplateIndexedNode

class TemplateStarNode(TemplateIndexedNode):

    def __init__(self, index=1):
        super().__init__(index)

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)

        if conversation.has_current_question():

            current_question = conversation.current_question()

            current_sentence = current_question.current_sentence()

            matched_context = current_sentence.matched_context
            if matched_context is None:
                YLogger.error(client_context, "Star node has no matched context for clientid %s", client_context.userid)
                resolved = ""
            else:
                try:
                    resolved = matched_context.star(self.index)
                    if resolved is None:
                        YLogger.error(client_context, "Star index not in range [%d]", self.index)
                        resolved = ""
                except Exception:
                    YLogger.error(client_context, "Star index not in range [%d]", self.index)
                    resolved = ""
        else:
            resolved = ""

        YLogger.debug(client_context, "Star Node [%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        string = "STAR"
        string += self.get_index_as_str()
        return string

    def to_xml(self, client_context):
        xml = "<star"
        xml += self.get_index_as_xml()
        xml += ">"
        xml += "</star>"
        return xml

    #######################################################################################################
    # INDEX_ATTRIBUTE ::== index="NUMBER"
    # STAR_EXPRESSION ::== <star( INDEX_ATTRIBUTE)/> | <star><index>TEMPLATE_EXPRESSION</index></star>

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "index", "1")
