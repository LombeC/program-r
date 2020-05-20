import numpy as np

DISTRIBUTION_SIZE = 10
NEGATIVE_THRESHOLD = -2

class SentimentData():

    def __init__(self):
        self._sentiment_values = np.zeros(DISTRIBUTION_SIZE)
        self._sentiment_distributions = []
        self._final_sentiment_values = []
        self._rolling_sentiment = 0
        self._neg_thresh = NEGATIVE_THRESHOLD
        self._threshold_reached = False
        self.init_weight()

    @property
    def values(self):
        return self._sentiment_values

    @property
    def sentiment_distributions(self):
        return self._sentiment_distributions

    @property
    def last_sentiment_value(self):
        return self._sentiment_values[-1]

    @property
    def final_sentiment_values(self):
        return self._final_sentiment_values

    @property
    def last_final_sentiment_value(self):
        return self._final_sentiment_values[-1]

    def init_weight(self):
        # self._weight = (DISTRIBUTION_SIZE*2) / 100
        self._weight = np.arange(0.1, 1.1, 0.1)
        print("Weight: {}".format(self._weight))        

    # NOTE: Most recent sentiment is the last element in self._sentiment_values
    def append_sentiment(self, sentiment): 
        try:
            if sentiment is None:
                # print("None sentiment trying to be added. Ignore")
                return

            self._sentiment_values = np.append(self._sentiment_values, sentiment)
            if len(self._sentiment_values) > DISTRIBUTION_SIZE:
                self._sentiment_values = np.delete(self._sentiment_values, 0)
                self.update_rolling()
        except Exception as ex:
            print("Error appending sentiment: {}".format(ex))

    def append_sentiment_distribution(self, sentiment_distribution):
        self._sentiment_distributions.append(sentiment_distribution)

    def append_final_sentiment(self, final_sentiment):
        self._final_sentiment_values.append(final_sentiment)

    def update_rolling(self):
        try:
            self._rolling_sentiment = np.sum(np.multiply(self._sentiment_values, self._weight))

            # for sent in self._sentiment_values:
            #     if sent is None:
            #         pass
            #     else:
            #         self._rolling_sentiment += sent * self._weight
            #         self._weight += 0.1
            
            # Trigger for a low sentiment
            if self._rolling_sentiment <= self._neg_thresh:
                self.threshold_reached()
                self.init_weight()
                self._rolling_sentiment = 0
                # self.append_sentiment(0.5)
            else:
                self._threshold_reached = False
                self.init_weight()

        except Exception as ex:
            print("Error updating rolling sentiment: {}".format(ex))

    def threshold_reached(self):
        # print("THRESHOLD REACHED: {}".format(self._rolling_sentiment))
        self._threshold_reached = True