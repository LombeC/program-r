from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.template.nodes.richmedia.card import TemplateCardNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils


class TemplateCarouselNode(TemplateNode):

    def __init__(self):
        super().__init__()
        self._cards = []

    def resolve_to_string(self, client_context):
        str = "<carousel>"
        for card in self._cards:
            str += card.resolve_to_string(client_context)
        str += "</carousel>"
        return str

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "[CAROUSEL] %d" % (len(self._cards))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'card':
                card_class = graph.get_node_class_by_name("card")
                card = card_class()
                card.parse_expression(graph, child)
                self._cards.append(card)
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

