

class SentimentData():

    def __init__(self):
        self._sentiment_values = []
        self._sentiment_distributions = []
        self._final_sentiment_values = []

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

    def append_sentiment(self, sentiment):
        self._sentiment_values.append(sentiment)

    def append_sentiment_distribution(self, sentiment_distribution):
        self._sentiment_distributions.append(sentiment_distribution)

    def append_final_sentiment(self, final_sentiment):
        self._final_sentiment_values.append(final_sentiment)


