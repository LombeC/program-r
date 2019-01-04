from programrtest.parser.base import ParserTestsBaseClass

from programr.parser.exceptions import ParserException

from programr.parser.pattern.nodes.base import PatternNode
from programr.parser.template.nodes.base import TemplateNode
from programr.parser.pattern.nodes.root import PatternRootNode
from programr.parser.pattern.nodes.word import PatternWordNode
from programr.parser.pattern.nodes.priority import PatternPriorityWordNode
from programr.parser.pattern.nodes.topic import PatternTopicNode
from programr.parser.pattern.nodes.that import PatternThatNode
from programr.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programr.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode
from programr.parser.pattern.nodes.set import PatternSetNode
from programr.parser.pattern.nodes.iset import PatternISetNode
from programr.parser.pattern.nodes.bot import PatternBotNode
from programr.parser.pattern.nodes.regex import PatternRegexNode
from programr.parser.pattern.nodes.template import PatternTemplateNode


class PatternRootNodeTests(ParserTestsBaseClass):

    def test_init(self):
        node = PatternRootNode()
        self.assertIsNotNone(node)

        self.assertTrue(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertTrue(node.equivalent(PatternRootNode()))
        self.assertEqual(node.to_string(), "ROOT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]")

        node.add_child(PatternNode())
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "ROOT [*] [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)]")

    def test_multiple_roots(self):
        node1 = PatternRootNode()
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertTrue(str(raised.exception).startswith("Cannot add root node to existing root node"))

    def test_root_added_to_child(self):
        node1 = PatternWordNode("test")
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertTrue(str(raised.exception).startswith("Cannot add root node to child node"))

    def test_root_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternRootNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add root node to existing root node")

    def test_template_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to root node")

    def test_topic_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternTopicNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add topic node to root node")

    def test_that_to_root(self):
        node1 = PatternRootNode()
        node2 = PatternThatNode()

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add that node to root node")

    def test_multiple_templates(self):
        node1 = PatternTemplateNode(TemplateNode())
        node2 = PatternTemplateNode(TemplateNode())

        with self.assertRaises(ParserException) as raised:
            node1.can_add(node2)
        self.assertEqual(str(raised.exception), "Cannot add template node to template node")

    def test_to_string(self):
        node1 = PatternRootNode()
        self.assertEquals("ROOT ", node1.to_string(verbose=False))
        self.assertEquals("ROOT [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]", node1.to_string(verbose=True))

        node2 = PatternRootNode("testid")
        self.assertEquals("ROOT ", node2.to_string(verbose=False))
        self.assertEquals("ROOT [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)]", node2.to_string(verbose=True))

    def test_equivalent_userid(self):
        node1 = PatternRootNode()
        node2 = PatternRootNode()
        node3 = PatternRootNode(userid="testuser")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))

    def test_remove_children_with_userid(self):
        root = PatternRootNode()

        root.add_child(PatternWordNode("test1"))
        root.add_child(PatternWordNode("test2", userid="user1"))
        root.add_child(PatternWordNode("test3", userid="user1"))
        root.add_child(PatternWordNode("test4", userid="user2"))

        self.assertEquals(4, len(root.children))

        root.remove_children_with_userid("user1")

        self.assertEquals(2, len(root.children))

    def test_remove_all_types_children_with_userid(self):
        root = PatternRootNode()

        root.add_child(PatternPriorityWordNode("test1", userid="user1"))
        root.add_child(PatternWordNode("test2", userid="user1"))
        root.add_child(PatternZeroOrMoreWildCardNode('^', userid="user1"))
        root.add_child(PatternZeroOrMoreWildCardNode('#', userid="user1"))
        root.add_child(PatternOneOrMoreWildCardNode('_', userid="user1"))
        root.add_child(PatternOneOrMoreWildCardNode('*', userid="user1"))

        self.assertEquals(1, len(root.priority_words))
        self.assertIsNotNone(root._0ormore_hash)
        self.assertIsNotNone(root._1ormore_underline)
        self.assertEquals(1, len(root.children))
        self.assertIsNotNone(root._0ormore_arrow)
        self.assertIsNotNone(root._1ormore_star)

        root.remove_children_with_userid("user1")

        self.assertEquals(0, len(root.priority_words))
        self.assertIsNone(root._0ormore_hash)
        self.assertIsNone(root._1ormore_underline)
        self.assertEquals(0, len(root.children))
        self.assertIsNone(root._0ormore_arrow)
        self.assertIsNone(root._1ormore_star)
