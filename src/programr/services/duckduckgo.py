from programr.utils.logging.ylogger import YLogger
import json

from programr.services.service import Service
from programr.services.requestsapi import RequestsAPI


class DuckDuckGoAPI(object):

    def __init__(self, request_api=None):
        if request_api is None:
            self._requests_api = RequestsAPI()
        else:
            self._requests_api = request_api

    # Provide a summary of a single article
    def ask_question(self, url, question, num_responses=1):
        # http://api.duckduckgo.com/?q=DuckDuckGo&format=json

        payload = {'q': question, 'format': 'json'}
        response = self._requests_api.get(url, params=payload)

        if response is None:
            raise Exception("No response from DuckDuckGo service")

        if response.status_code != 200:
            raise Exception("Error response from DuckDuckGo service [%d]"%response.status_code)

        json_data = json.loads(response.text)
        if 'RelatedTopics' not in json_data:
            raise Exception("Invalid response from DuckDuckGo service, 'RelatedTopcis' missing from payload")
        topics = json_data['RelatedTopics']

        if len(topics) == 0:
            raise Exception("Invalid response from DuckDuckGo service, no topics in payload")

        if len(topics) < num_responses:
            num_responses = len(topics)

        responses = []
        for i in range(num_responses):
            if 'Text' in topics[i]:
                sentences = topics[i]['Text'].split(".")
                responses.append(sentences[0])

        return ". ".join(responses)


class DuckDuckGoService(Service):

    def __init__(self, config=None, api=None):
        Service.__init__(self, config)

        if api is None:
            self._api = DuckDuckGoAPI()
        else:
            self._api = api

        self._url = None
        if config._url is None:
            raise Exception("Undefined url parameter")
        else:
            self._url = config.url

    def ask_question(self, client_context, question: str):
        try:
            return self._api.ask_question(self._url, question)
        except Exception as e:
            YLogger.error(client_context, "General error querying DuckDuckGo for question [%s] - [%s]", question, str(e))
        return ""