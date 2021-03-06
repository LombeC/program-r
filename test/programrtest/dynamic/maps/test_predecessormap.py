import unittest

from programr.dynamic.maps.predecessor import PredecessorMap
from programr.context import ClientContext

from programrtest.aiml_tests.client import TestClient


class TestPredecessorMaps(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "testid")

    def test_predecessor(self):
        map = PredecessorMap(None)
        self.assertEqual("1", map.map_value(self._client_context, "2"))

    def test_predecessor_text(self):
        map = PredecessorMap(None)
        self.assertEqual("", map.map_value(self._client_context, "two"))

