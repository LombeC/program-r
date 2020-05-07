import numpy as np

class SentimentData():

    def __init__(self):
        self._sentiment_values = np.zeros(10)
        self._sentiment_distributions = []
        self._final_sentiment_values = []
        self._rolling_sentiment = 0

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

    # NOTE: Most recent sentiment is the last element in self._sentiment_values
    def append_sentiment(self, sentiment): 
        try:
            if sentiment is None:
                print("None sentiment trying to be added. Ignore")
                return
                
            print("In SentimentData: {}".format(sentiment))
            self._sentiment_values = np.append(self._sentiment_values, sentiment)
            if len(self._sentiment_values) > 10:
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
            dampening = 0.1
            for sent in self._sentiment_values:
                if sent is None:
                    pass
                else:
                    self._rolling_sentiment += sent * dampening
                    dampening += 0.1
        except Exception as ex:
            print("Error updating rolling sentiment: {}".format(ex))


