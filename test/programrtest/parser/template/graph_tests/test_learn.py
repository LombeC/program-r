import xml.etree.ElementTree as ET

from programr.parser.template.nodes.base import TemplateNode
from programr.parser.template.nodes.learn import TemplateLearnNode, LearnCategory
from programr.context import ClientContext
from programr.bot import Bot
from programr.config.bot.bot import BotConfiguration

from programrtest.aiml_tests.client import TestClient
from programrtest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphLearnTests(TemplateGraphTestClient):

    def test_learn_simple(self):
        
        client_context1 = ClientContext(TestClient(), "testid")
        client_context1.bot = Bot(BotConfiguration())
        client_context1.brain = client_context1.bot.brain

        template = ET.fromstring("""
			<template>
				<learn>
				    <category>
				        <pattern>HELLO <eval>WORLD</eval> <iset>THERE, NOW</iset></pattern>
				        <template>HIYA</template>
				    </category>
				</learn>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)
        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertEqual(len(ast.children), 1)

        learn_node = ast.children[0]
        self.assertIsNotNone(learn_node)
        self.assertIsInstance(learn_node, TemplateLearnNode)
        self.assertEqual(1, len(learn_node.children))
        self.assertIsInstance(learn_node.children[0], LearnCategory)
        self.assertIsNotNone(learn_node.children[0].pattern)
        self.assertIsInstance(learn_node.children[0].pattern, ET.Element)
        self.assertIsNotNone(learn_node.children[0].topic)
        self.assertIsInstance(learn_node.children[0].topic, ET.Element)
        self.assertIsNotNone(learn_node.children[0].that)
        self.assertIsInstance(learn_node.children[0].that, ET.Element)
        self.assertIsNotNone(learn_node.children[0].template)
        self.assertIsInstance(learn_node.children[0].template, TemplateNode)

        resolved = learn_node.resolve(client_context1)
        self.assertEqual(resolved, "")

        response = client_context1.bot.ask_question(client_context1, "HELLO WORLD THERE")
        self.assertEqual("HIYA", response)

    def test_learn_multi_user(self):
        client_context1 = ClientContext(TestClient(), "testid")
        client_context1.bot = Bot(BotConfiguration())
        client_context1.brain = client_context1.bot.brain

        template = ET.fromstring("""
			<template>
				<learn>
				    <category>
				        <pattern>HELLO THERE ONE</pattern>
				        <template>HIYA ONE</template>
				    </category>
				</learn>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context1)

        response = client_context1.bot.ask_question(client_context1, "HELLO THERE ONE")
        self.assertEqual("HIYA ONE", response)

        client_context2 = ClientContext(TestClient(), "testid")
        client_context2.bot = Bot(BotConfiguration())
        client_context2.brain = client_context2.bot.brain

        template = ET.fromstring("""
			<template>
				<learn>
				    <category>
				        <pattern>HELLO THERE TWO</pattern>
				        <template>HIYA TWO</template>
				    </category>
				</learn>
			</template>
			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context2)

        response = client_context2.bot.ask_question(client_context2, "HELLO THERE TWO")
        self.assertEqual("HIYA TWO", response)

        # Now try and ask each others questions

        response = client_context1.bot.ask_question(client_context1, "HELLO THERE TWO")
        self.assertEqual("", response)

        response = client_context2.bot.ask_question(client_context2, "HELLO THERE ONE")
        self.assertEqual("", response)

    def test_multiple_patterns(self):
        client_context1 = ClientContext(TestClient(), "testid")
        client_context1.bot = Bot(BotConfiguration())
        client_context1.brain = client_context1.bot.brain

        template = ET.fromstring("""
        			<template>
        				<learn>
        				    <category>
        				        <pattern>HELLO THERE</pattern>
        				        <template>HIYA ONE</template>
        				    </category>
        				</learn>
        			</template>
        			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context1)

        response = client_context1.bot.ask_question(client_context1, "HELLO THERE")
        self.assertEqual("HIYA ONE", response)

        client_context2 = ClientContext(TestClient(), "testid")
        client_context2.bot = Bot(BotConfiguration())
        client_context2.brain = client_context2.bot.brain

        template = ET.fromstring("""
        			<template>
        				<learn>
        				    <category>
        				        <pattern>HELLO THERE</pattern>
        				        <template>HIYA TWO</template>
        				    </category>
        				</learn>
        			</template>
        			""")

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context2)

        response = client_context2.bot.ask_question(client_context2, "HELLO THERE")
        self.assertEqual("HIYA TWO", response)

