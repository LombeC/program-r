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
from transformers import (RobertaTokenizer, RobertaForSequenceClassification, InputExample,
                          glue_convert_examples_to_features, DistilBertTokenizer, DistilBertForSequenceClassification)

from programr.config.brain.semantic_similarity import BrainSemanticSimilarityConfiguration
from programr.nlp.semantic.semantic_similarity import DistilRobertaSemanticSimilarity
from programr.nlp.semantic.sentiment_analysis import DistilBertSentimentAnalysis
from programr.services.wikipediaservice import WikipediaAPI, WikipediaService


server = SimpleXMLRPCServer(('localhost', 3000), logRequests=True)

def wiki_summary(title, sentences=2, chars=0, auto_suggest=True, redirect=False):
    try:
        print("in the server")
        return wikipedia.summary(title, sentences, chars, auto_suggest, redirect)
    except:
        return "No result"

def check_sentiment(text):
    tokenizer = DistilBertTokenizer.from_pretrained('./libs/pretrain_distillbert_full_sst')
    model = DistilBertForSequenceClassification.from_pretrained('./libs/pretrain_distillbert_full_sst')
    sentiment_classifier = SentimentClassifer(model, tokenizer)
    result = sentiment_classifier(text)
    sentiment = max(result, key=result.get)
    sentiment_distribution = list(result.values())
    print("sentiment of {}: {}".format(text, sentiment))
    return sentiment

def get_semantic_similarity(text1, text2):
    # model = RobertaForSequenceClassification.from_pretrained('./libs/pretrain_roberta_model')
    # print("model created...")
    
    # tokenizer = RobertaTokenizer.from_pretrained('./libs/pretrain_roberta_model')
    # print("tokenizer created...")

    config = BrainSemanticSimilarityConfiguration()
    config._model_dir = "./libs/pretrain_roberta_model"

    semantic_similarity_classifier = DistilRobertaSemanticSimilarity(config)
    result = semantic_similarity_classifier.similarity_with_concept(text1, text2)
    print("similarity score: {}".format(result))
    return result

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

def get_weather(location="Denver, USA"):
    with open("./src/programr/rpcservices/api_key_config.yaml", 'r') as stream:
        data = yaml.safe_load(stream)
        api_key = data['weather']
        observation = OWM(api_key).weather_at_place(location)
        weather = observation.get_weather()
        return str(weather.get_temperature(unit='fahrenheit')['temp'])

def register_functions(server):
    server.register_function(wiki_summary)
    server.register_function(check_sentiment)
    server.register_function(get_news)
    server.register_function(get_weather)
    server.register_function(get_semantic_similarity)

if __name__ == "__main__":
    try:
        print('Serving...')
        register_functions(server)
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting")