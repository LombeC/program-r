import json
import requests

from programr.utils.logging.ylogger import YLogger
from programr.dynamic.variables.variable import DynamicVariable

class GetSentiment(DynamicVariable):

    def __init__(self, config):
        super().__init__(config)

    def get_value(self, client_context, value=None):
        userid = client_context.userid
        variables = client_context.bot.conversations[userid].properties
        bot = client_context.bot
        nlp = client_context.brain.nlp
        text = variables["data"]
        #todo the problem with some forms of text like

        #if bot.configuration.emotive:
        #YLogger.info(self, "bot is in emotive mode")
        try:
            # print(f"in sentiment_analysis, text: {text}")
            # NOTE: On only 2 occasions text has been none when trying to analyze sentiment
            #       When this occured the question was "why just say...", a misinterpretation from kaldi
            
            # FIXME: We need a more sophisticated error check, fix after demo.
            # if text is None:
            #     return sentiment = "neutral"

            # TODO: Finish this implementation and remove function call below this segment
            response = requests.post('http://localhost:5000/api/rest/v1.0/sentiment',  json={'question': text})
            response = json.loads(response.text)
            sentiment = response['response']
            sentiment = sentiment[0]
            sentiment_distribution = sentiment[1]

            # sentiment, sentiment_distribution = nlp.sentiment_analysis.get_sentence_sentiment(text)
        except Exception as exception:
            YLogger.exception(self, "sentiment analysis module broke", exception)
            raise exception

        sentiment_value = None
        final_sentiment_value = None

        if bot.facial_expression_recognition is not None:
            if len(bot.facial_expression_recognition.values):
                last_fer_value = 0#bot.facial_expression_recognition.last_fer_value

                #the logic of mixing fer and sentiment goes here
                alpha = nlp.sentiment_analysis.alpha
                positive_threshold = nlp.sentiment_analysis.positive_threshold
                negative_threshold = nlp.sentiment_analysis.negative_threshold

                sentiment_value = nlp.sentiment_analysis.expected_sentiment_value(sentiment_distribution)

                print("FER: ", last_fer_value)
                print("Sentiment:", sentiment_value)

                final_sentiment_value = alpha * last_fer_value + (1-alpha)*sentiment_value
                print("Final sentiment: ", final_sentiment_value)
                if final_sentiment_value > positive_threshold:
                    sentiment = "positive"
                elif final_sentiment_value < positive_threshold and final_sentiment_value > negative_threshold:
                    sentiment = "neutral"
                else:
                    sentiment = "negative"

        else:
            if sentiment == "positive":
                sentiment_value = 1
                final_sentiment_value = 1
            elif sentiment == "neutral":
                sentiment_value = 0
                final_sentiment_value = 0
            elif sentiment == "negative":
                sentiment_value = -1
                final_sentiment_value = -1


        bot.sentiment.append_sentiment(sentiment_value)
        bot.sentiment.append_sentiment_distribution(sentiment_distribution)
        bot.sentiment.append_final_sentiment(final_sentiment_value)

        if bot.configuration.emotive:
            YLogger.info(self, "bot is in emotive mode")
        else:
            YLogger.info(self, "bot is in non emotive mode")
            sentiment = "neutral"

        print("In GetSentiment sentiment: {}".format(sentiment))
        return sentiment
