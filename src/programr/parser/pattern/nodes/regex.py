from programr.utils.logging.ylogger import YLogger
import re

from programr.parser.pattern.nodes.base import PatternNode
from programr.parser.pattern.matcher import EqualsMatch
from programr.parser.exceptions import ParserException


class PatternRegexNode(PatternNode):

    def __init__(self, attribs, text, userid='*'):
        PatternNode.__init__(self, userid)
        self._pattern_text = None
        self._pattern_template = None
        self._pattern = None
        if 'pattern' in attribs:
            self._pattern_text = attribs['pattern']
        elif 'template' in attribs:
            self._pattern_template = attribs['template']
        elif text:
            self._pattern_text = text
        else:
            raise ParserException("Invalid regex node, neither pattern or template specified as attribute or text")

        if self._pattern_text is not None:
            self._pattern = re.compile(self._pattern_text)

    @property
    def pattern(self):
        return self._pattern

    @property
    def pattern_text(self):
        return self._pattern_text

    @property
    def pattern_template(self):
        return self._pattern_template

    def is_regex(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if self._pattern_template is not None:
            if include_user is True:
                string += '<regex userid="%s" template="%s">'%(self.userid, self._pattern_template)
            else:
                string += '<regex template="%s">'% self._pattern_template
        else:
            if include_user is True:
                string += '<regex userid="%s" pattern="%s">'%(self.userid, self._pattern_text)
            else:
                string += '<regex pattern="%s">' % self._pattern_text
        string += super(PatternRegexNode, self).to_xml(client_context)
        string += "</regex>\n"
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            if self._pattern_template is not None:
                return "REGEX [%s] [%s] template=[%s]" % (self.userid, self._child_count(verbose), self._pattern_template)
            return "REGEX [%s] [%s] pattern=[%s]" % (self.userid, self._child_count(verbose), self._pattern_text)

        if self._pattern_template is not None:
            return "REGEX template=[%s]" % self._pattern_template
        return "REGEX pattern=[%s]" % self._pattern_text

    def equivalent(self, other):
        if other.is_regex():
            if self.userid == other.userid:
                if self._pattern_template is not None:
                    if other.pattern_template is not None:
                        return bool(self._pattern_template == other.pattern_template)
                else:
                    if other.pattern is not None:
                        return bool(self.pattern == other.pattern)
        return False

    def equals(self, client_context, words, word_no):
        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        if self._pattern_template is not None:
            template = client_context.brain.regex_templates[self._pattern_template]
            if template is not None:
                result = template.match(word)
                if result is not None:
                    YLogger.debug(client_context, "Match word [%s] regex", word)
                    return EqualsMatch(True, word_no, word)
                else:
                    YLogger.error(client_context, "No word [%s] matched regex", word)
                    return EqualsMatch(False, word_no)
            else:
                return EqualsMatch(False, word_no)
        else:
            result = self.pattern.match(word)
            if result is not None:
                YLogger.debug(client_context, "Match word [%s] regex", word)
                return EqualsMatch(True, word_no, word)
            else:
                YLogger.error(client_context, "No word [%s] matched regex", word)
                return EqualsMatch(False, word_no)
