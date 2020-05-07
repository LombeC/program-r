import unittest
import os
import numpy as np

from programr.robot.sentimentdata import SentimentData

class SentimentDataTests(unittest.TestCase):
    
    def test_init_sentiment_values(self):
        data = SentimentData()
        expected = np.array([0,0,0,0,0,0,0,0,0,0])
        self.assertEqual(expected.all(), data._sentiment_values.all())

    def test_append_positive(self):
        data = SentimentData()
        data.append_sentiment(1)
        expected = np.array([0,0,0,0,0,0,0,0,0,1])
        self.assertEqual(expected.all(), data._sentiment_values.all())

    def test_threshold_bool(self):
        data = SentimentData()
        data.append_sentiment(-0.81)
        expected = True
        self.assertEqual(expected, data._threshold_reached)

if __name__ == '__main__':
    unittest.main()