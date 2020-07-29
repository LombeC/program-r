from programr.utils.logging.ylogger import YLogger

from programr.parser.template.nodes.base import TemplateNode


class TemplatePersonNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        try:
            string = self.resolve_children_to_string(client_context)
            resolved = client_context.brain.persons.personalise_string(string)
            # print("templatenode: {}".format(client_context.brain.persons.person(resolved)))
            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "PERSON"

    def to_xml(self, client_context):
        xml = "<person>"
        xml += self.children_to_xml(client_context)
        xml += "</person>"
        return xml

    #######################################################################################################
    # PERSON_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def add_default_star(self):
        return True

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
