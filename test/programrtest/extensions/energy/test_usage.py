import unittest

from programr.extensions.energy.usage import EnergyUsageExtension
from programr.context import ClientContext

from programrtest.aiml_tests.client import TestClient

class EnergyUsageExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self.context = client.create_client_context("testid")

    def test_usage(self):

        usage = EnergyUsageExtension()
        self.assertIsNotNone(usage)

        result = usage.execute(self.context, "NOW")
        self.assertIsNotNone(result)
        self.assertEqual("0 0 KWh", result)