import unittest
import os

from programr.context import ClientContext
from programrtest.aiml_tests.client import TestClient


class BotAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BotAIMLTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.brain_config[0].brain_config[0].files.aiml_files._files = [os.path.dirname(__file__)]


class BotAIMLTests(unittest.TestCase):

    def setUp(self):
        client = BotAIMLTestClient()
        self._client_context = client.create_client_context("testid")

        self._client_context.bot.brain.properties.load_from_filename("./properties.txt")
        # load_from_text("""
        #     url:http://www.keithsterling.com/aiml
        #     name:KeiffBot 1.0
        #     firstname:Keiff
        #     middlename:AIML
        #     lastname:BoT
        #     fullname:KeiffBot
        #     email:info@keiffbot.org
        #     gender:male
        #     botmaster:Keith Sterling
        #     organization:keithsterling.com
        #     version:0.0.1
        #     birthplace:Edinburgh, Scotland
        #     job:mobile virtual assistant
        #     species:robot
        #     birthday:September 9th
        #     birthdate:September 9th, 2016
        #     sign:Virgo
        #     logo:<img src="http://www.keithsterling.com/aiml/logo.png" width="128"/>
        #     religion:Atheist
        #     default-get:unknown
        #     default-property:unknown
        #     default-map:unknown
        #     learn-filename:learn.aiml
        # """)

    
    def test_bot_youare_lazy(self):
        response = self._client_context.bot.ask_question(self._client_context,  "YOU ARE LAZY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Only on Sunday mornings!")

    def test_bot_whats_your_hobby(self):
        response = self._client_context.bot.ask_question(self._client_context,  "WHAT S YOUR HOBBY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "My hobby is chatting online with nice folks like yourself.")

    
    def test_bot_property_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context,  "BOT PROPERTY XXX")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_url(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY URL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "http://www.keithsterling.com/aiml")

    def test_bot_property_name(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "KeiffBot 1.0")

    def test_bot_property_firstname(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY FIRSTNAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keiff")

    def test_bot_property_middlename(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY MIDDLENAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIML")

    def test_bot_property_lastname(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY LASTNAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "BoT")

    def test_bot_property_email(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY EMAIL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "info@keiffbot.org")

    def test_bot_property_gender(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "male")

    def test_bot_property_botmaster(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BOTMASTER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keith Sterling")

    def test_bot_property_organisation(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY ORGANISATION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "keithsterling.com")

    def test_bot_property_version(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY VERSION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "0.0.1")

    def test_bot_property_birthplace(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BIRTHPLACE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Edinburgh, Scotland")

    def test_bot_property_birthday(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BIRTHDAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "September 9th")

    def test_bot_property_sign(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY SIGN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Virgo")

    def test_bot_property_birthdate(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BIRTHDATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "September 9th, 2016")

    def test_bot_property_job(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY JOB")
        self.assertIsNotNone(response)
        self.assertEqual(response, "mobile virtual assistant")

    def test_bot_property_species(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY SPECIES")
        self.assertIsNotNone(response)
        self.assertEqual(response, "robot")

    def test_bot_property_religion(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY RELIGION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "No religion, I am an Atheist")

    def test_bot_property_logo(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY LOGO")
        self.assertIsNotNone(response)
        self.assertEqual(response, '<img src="http://www.keithsterling.com/aiml/logo.png" width="128"/>')

    def test_bot_property_default_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY DEFAULT GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_default_map(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY DEFAULT MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_default_property(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY DEFAULT PROPERTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "unknown")

    def test_bot_property_default_learn_filename(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY LEARN FILENAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "learn.aiml")
