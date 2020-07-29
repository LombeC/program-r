from programr.utils.logging.ylogger import YLogger
import datetime
from datetime import timezone

from programr.parser.exceptions import ParserException
from programr.parser.template.nodes.attrib import TemplateAttribNode


class TemplateDateNode(TemplateAttribNode):

    def __init__(self, date_format=None):
        TemplateAttribNode.__init__(self)
        if date_format is None:
            self._format = "%c"
        else:
            self._format = date_format

    def resolve_to_string(self, client_context):
        time_now = datetime.datetime.now()
        time_now.replace(tzinfo=timezone.utc)
        resolved = time_now.strftime(self._format)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "DATE format=%s" % (self._format)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'format':
            raise ParserException("Invalid attribute name %s for this node" % (attrib_name))
        self._format = attrib_value

    def to_xml(self, client_context):
        xml = '<date format="%s" >' % self._format
        xml += self.children_to_xml(client_context)
        xml += "</date>"
        return xml

    #######################################################################################################
    # DATE_ATTRIBUTES ::== (format="LISP_DATE_FORMAT") | (jformat="JAVA DATE FORMAT")
    # DATE_ATTRIBUTE_TAG ::== <format>TEMPLATE_EXPRESSION</format> | <jformat>TEMPLATE_EXPRESSION</jformat>
    # DATE_EXPRESSION ::== <date( DATE_ATTRIBUTES)*/> | <date>(DATE_ATTRIBUTE_TAG)</date>
    # Pandorabots supports three extension attributes to the date element in templates:
    #     	locale
    #       format
    #       timezone

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "format", "%c")
