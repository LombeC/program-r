from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.richmedia.list import TemplateListNode


class TemplateOrderedListNode(TemplateListNode):

    def __init__(self):
        super().__init__()

    def resolve_to_string(self, client_context):
        str = "<olist>"
        str += self.resolve_list_items(client_context)
        str += "</olist>"
        return str

    def to_string(self):
        return "[OLIST] %d" % (len(self._items))

