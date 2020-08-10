import os
import time
import requests
import wikipedia
import numpy as np
import yaml
from yaml import load, dump

from flask import Flask, make_response, jsonify
from xmlrpc.server import SimpleXMLRPCServer
from newsapi import NewsApiClient
from pyowm import OWM

import torch 
from transformers import (RobertaTokenizer, RobertaForSequenceClassification, InputExample, pipeline,
                          glue_convert_examples_to_features, DistilBertTokenizer, DistilBertForSequenceClassification)

from programr.rpcservices.models import DistilBertSentimentAnalysis, DistilRobertaSemanticSimilarity
from programr.services.wikipediaservice import WikipediaAPI, WikipediaService


server = SimpleXMLRPCServer(('localhost', 3000), logRequests=True)

def wiki_summary(title, sentences=2, chars=0, auto_suggest=True, redirect=False):
    try:
        print("in the server")
        return wikipedia.summary(title, sentences, chars, auto_suggest, redirect)
    except:
        return "No result"

def check_sentiment(text):
    try:
        sentiment_classifier = DistilBertSentimentAnalysis()
        sentiment, sentiment_distribution = sentiment_classifier.get_sentence_sentiment(text)
        print("sentiment of {}: {}".format(text, sentiment))
        return sentiment, sentiment_distribution
    except Exception as ex:
        print("Exception caught trying to analyze sentiment - {}".format(ex))

def get_summary(text):
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(text, min_length=1, max_length=30)
        return summary[0]['summary_text']
    except Exception as ex:
        print("Exception caught trying to summarize text - {}".format(ex))

def get_semantic_similarity_concept(text, concept):
    try:
        similarity_classifier = DistilRobertaSemanticSimilarity()
        result = similarity_classifier.similarity_with_concept(text, concept)
        print("similarity score between \'{}\' and \'{}\': {}".format(text, concept, result))
        return result
    except Exception as ex:
        print("Exception caught getting sentence similiarity - {}".format(ex))

def get_semantic_similarity_concepts(text, concepts):
    try:
        similarity_classifier = DistilRobertaSemanticSimilarity()
        result = similarity_classifier.similarity_with_concepts(text, concepts)
        print("similarity score between \'{}\' and \'{}\': {}".format(text, concepts, result))
        return result
    except Exception as ex:
        print("Exception caught getting sentence similiarity - {}".format(ex))

def get_news(headline_index=0, sources=None, country=None):
    try:
        with open("./src/programr/rpcservices/api_key_config.yaml", 'r') as stream:
            data = yaml.safe_load(stream)
            headers = data['news']['headers']
            url = data['news']['url']
            
            response = requests.request("GET", url=url, headers=headers, params=None)
            headline_dict = response.json()
            headline = headline_dict['value'][headline_index]['name']
            return headline
    except Exception as ex:
        print("error getting request. {}".format(ex))
        return ""

def get_weather_temperature(location="Denver, USA"):
    with open("./src/programr/rpcservices/api_key_config.yaml", 'r') as stream:
        data = yaml.safe_load(stream)
        api_key = data['weather']
        observation = OWM(api_key).weather_at_place(location)
        weather = observation.get_weather()
        return str(weather.get_temperature(unit='fahrenheit')['temp'])

def get_weather_status(location="Denver, USA"):
    try:
        with open("./src/programr/rpcservices/api_key_config.yaml", 'r') as stream:
            data = yaml.safe_load(stream)
            api_key = data['weather']
            observation = OWM(api_key).weather_at_place(location)
            print("observation: {}".format(type(observation)))
            print("observation: {}".format(observation))
            weather = observation.get_weather()
            return str(weather.get_status())
    except Exception as ex:
        print("Exception found getting weather status - {}".format(ex))


def register_functions(server):
    server.register_function(wiki_summary)
    server.register_function(check_sentiment)
    server.register_function(get_news)
    server.register_function(get_weather_temperature)
    server.register_function(get_weather_status)
    server.register_function(get_semantic_similarity_concept)
    server.register_function(get_semantic_similarity_concepts)
    server.register_function(get_summary)

if __name__ == "__main__":
    try:
        print('Serving...')
        register_functions(server)
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")