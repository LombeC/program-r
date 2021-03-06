from programr.utils.logging.ylogger import YLogger
import json

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.exceptions import ParserException
from programr.utils.text.text import TextUtils

class TemplateGetNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._local = False
        self._tuples = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def local(self):
        return self._local

    @local.setter
    def local(self, local):
        self._local = local

    @property
    def tuples(self):
        return self._tuples

    @tuples.setter
    def tuples(self, tuples):
        self._tuples = tuples

    @staticmethod
    #TODO Replace bot with client_context
    def get_default_value(bot):
        value = bot.brain.properties.property("default-get")
        if value is None:
            YLogger.error(None, "No property defined for default-get, checking defaults")

            value = bot.brain.configuration.defaults.default_get
            if value is None:
                YLogger.error(None, "No value defined for default default-get, returning 'unknown'")
                value = "unknown"

        return value

    @staticmethod
    def get_property_value(client_context, local, name):

        if local is True:

            value = None
            #TODO Why would you need this test, when is get_conversation(clientid) == None ?
            if client_context.bot.get_conversation(client_context) is not None:
                if client_context.bot.get_conversation(client_context).has_current_question():
                    value = client_context.bot.get_conversation(client_context).current_question().property(name)

        else:

            if name is not None and client_context.brain.dynamics.is_dynamic_var(name) is True:
                value = client_context.brain.dynamics.dynamic_var(client_context, name)
            else:
                value = client_context.bot.get_conversation(client_context).property(name)
                #if value is None:
                #    value = bot.brain.properties.property(name)

        if value is None:
            YLogger.error(client_context, "No property for [%s]", name)

            value = TemplateGetNode.get_default_value(client_context.bot)

        return value

    def resolve_variable(self, client_context):
        name = self.name.resolve(client_context)
        value = TemplateGetNode.get_property_value(client_context, self.local, name)

        if self.local:
            YLogger.debug(client_context, "[%s] resolved to local: [%s] <= [%s]", self.to_string(), name, value)
        else:
            YLogger.debug(client_context, "[%s] resolved to global: [%s] <= [%s]", self.to_string(), name, value)

        #todo there should be a better way to do this
        value = value.title()

        return value

    def decode_tuples(self, tuples):
        if isinstance(tuples, str):
            return json.loads(tuples)
        else:
            return tuples

    def resolve_tuple(self, client_context):
        variables = self._name.resolve(client_context).split(" ")

        raw_tuples = self._tuples.resolve(client_context)
        try:
            tuples = self.decode_tuples(raw_tuples)
        except:
            tuples = []

        resolved = ""
        if tuples:

            if isinstance(tuples, list): # Is tuples an array of results in the form [[[subj, val],[pred, val],[obj, val]], [[subj, val],[pred, val],[obj, val]]...]

                if variables: #If we are asking for variables, pull out the vars
                    for atuple in tuples:
                        if isinstance(atuple[0], list) is True:
                            for pair in atuple:
                                for var in variables:
                                    if pair[0] == var:
                                        resolved += pair[1]
                                        resolved += " "
                        else:
                            for var in variables:
                                if atuple[0] == var:
                                    resolved += atuple[1]
                                    resolved += " "

                else:
                    for atuple in tuples:
                        resolved += atuple[0][1]
                        resolved += " "
                        resolved += atuple[1][1]
                        resolved += " "
                        resolved += atuple[2][1]
                        resolved += " "

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        return resolved

    def resolve_to_string(self, client_context):
        if self._tuples is None:
            value = self.resolve_variable(client_context)
        else:
            value = self.resolve_tuple(client_context)
        return value

    def resolve(self, client_context):
        try:
            client_context.bot.load_conversation(client_context.userid)
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        if self.tuples is None:
            if self.name is None:
                name = "None"
            else:
                name = self.name.to_string()
            return "[GET [%s] - %s]" % ("Local" if self.local else "Global", name)
        else:
            return "[GET [Tuples] - (%s)]" %self.name.to_string()

    def to_xml(self, client_context):
        if self.tuples is None:
            xml = "<get"
            if self.local:
                xml += ' var="%s"' % self.name.resolve(client_context)
            else:
                xml += ' name="%s"' % self.name.resolve(client_context)
            xml += " />"
        else:
            xml = "<get"
            xml += ' var="%s"' % self.name.resolve(client_context)
            xml += " >"
            xml += self.tuples.to_xml(client_context)
            xml += "</get>"
        return xml

    # ######################################################################################################
    # GET_PREDICATE_EXPRESSION ::==
    # <get name="WORD"/> |
    # <get><name>TEMPLATE_EXPRESSION</name></get> |
    # <get var=”WORD”> |
    # <get><var>WORD</var></get>

    def parse_expression(self, graph, expression):

        name_found = False
        var_found = False

        if 'name' in expression.attrib:
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'name')
            self.local = False
            name_found = True

        if 'var' in expression.attrib:
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'var')
            self.local = True
            var_found = True

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'name':
                self.name = self.parse_children_as_word_node(graph, child)
                self.local = False
                name_found = True

            elif tag_name == 'var':
                self.name = self.parse_children_as_word_node(graph, child)
                self.local = True
                var_found = True

            elif tag_name == "tuple":
                self._tuples = self.parse_children_as_word_node(graph, child)

        if name_found is False and var_found is False:
            raise ParserException("Invalid get, missing either name or var", xml_element=expression)

        if name_found is True and var_found is True:
            raise ParserException("Get node has both name AND var values", xml_element=expression)
