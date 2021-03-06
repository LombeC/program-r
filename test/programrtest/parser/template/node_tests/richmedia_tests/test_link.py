import xml.etree.ElementTree as ET

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.template.nodes.richmedia.link import TemplateLinkNode
from programr.parser.template.nodes.word import TemplateWordNode

from programrtest.parser.base import ParserTestsBaseClass

class TemplateLinkNodeTests(ParserTestsBaseClass):

    def test_link_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        link = TemplateLinkNode()
        link._text = TemplateWordNode("Servusai.com")
        link._url = TemplateWordNode("http://Servusai.com")

        root.append(link)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEquals("<link><text>Servusai.com</text><url>http://Servusai.com</url></link>", resolved)

        self.assertEquals("<link><text>Servusai.com</text><url>http://Servusai.com</url></link>", root.to_xml(self._client_context))

