import unittest

from programr.oob.oob import OutOfBandProcessor
import xml.etree.ElementTree as ET
from programr.context import ClientContext

from programrtest.aiml_tests.client import TestClient

class OutOfBandProcessorTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")

    def test_processor(self):
        oob_processor = OutOfBandProcessor()
        self.assertIsNotNone(oob_processor)
        self.assertIsNone(oob_processor._xml)

        oob_content = ET.fromstring("<something>process</something>")
        oob_processor.parse_oob_xml(oob_content)
        self.assertIsNotNone(oob_processor._xml)

        self.assertEqual("", oob_processor.execute_oob_command(self._client_context))

        self.assertEqual("", oob_processor.process_out_of_bounds(self._client_context, oob_content))
