import re
import requests
import wikipedia

from flask import Flask, make_response, jsonify

from programr.utils.logging.ylogger import YLogger
from programr.services.service import Service


class WikipediaAPI(object):

    # Provide a summary of a single article
    def summary(self, title, sentences=2, chars=0, auto_suggest=True, redirect=False):
        return wikipedia.summary(title, sentences, chars, auto_suggest, redirect)

    # Provide a list of articles matching the query
    # Use summary to return the neccassary action
    def search(self, query, results=10, suggestion=True):
        return wikipedia.search(query, results, suggestion)


class WikipediaService(Service):

    def __init__(self, config=None, api=None):
        Service.__init__(self, config)

        if api is None:
            self._api = WikipediaAPI()
        else:
            self._api = api

    def clean_summary(self, summary):
        # NOTE: Often wikipedia articles will have a listen plug-in in the summary.
        #       We need to make sure to get rid of extraneous characters
        #       so Ryan sounds natural, hence the cleaning.
        # print("BEFORE CLEANING")
        # print("summary: {}".format(summary))
        summary = summary.replace("(listen);", "")
        summary = summary.replace("(listen),", "")
        summary = summary.replace("(listen)", "")
        summary = summary.replace("IPA: ", "")
        summary = summary.replace("( )", "")

        summary.encode("ascii", errors="ignore")
        summary = re.sub('\[.*\]', '', summary)
        return summary

    def ask_question(self, client_context, question: str):
        try:
            words  = question.split()
            question = " ".join(words[1:])
            if words[0] == 'SUMMARY':
                # TODO: Replace below function call with a call to the server
                # search = self._api.summary(question, sentences=1)
                search = requests.post('http://localhost:5000/api/rest/v1.0/wiki',  json={'question': question})
                print(type(search))
                print(search)

                search = "According to wikipedia, " + self.clean_summary(search.text)
                # if search == "".join(search.split()):
                #     print("True")
                YLogger.debug(client_context, f"search in wikipediaservice: {search}")
            elif words[0] == 'SEARCH':
                results = self._api.search(question)
                search = ", ".join(results)
            else:
                YLogger.error(client_context, "Unknown Wikipedia command [%s]", words[0])
                search = ""
            return search
        except wikipedia.exceptions.DisambiguationError:
            YLogger.error(client_context, "Wikipedia search is ambiguous for your question [%s]", question)
            search = "Sorry, but I couldn't find anything on Wikipedia for your question: " + question
            return search
        except wikipedia.exceptions.PageError:
            YLogger.error(client_context, "No page on Wikipedia for your question [%s]", question)
        except Exception as ex:
            YLogger.error(client_context, "General error querying Wikipedia for your question [%s], Exception - [%s]", question, ex)
        return "Sorry, but I couldn't find anything on Wikipedia for your question about, " + question