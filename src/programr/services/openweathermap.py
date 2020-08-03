import requests

from flask import Flask, make_response, jsonify
from pyowm import OWM

from programr.utils.logging.ylogger import YLogger
from programr.services.service import Service


class WeatherAPI(object):

    def __init__(self, api_key):
        self.api_key = api_key

    # Get the current weather at a given location.
    # Location is a string of the form 'Denver, CO'
    def weather(self, location):
        return OWM(self.api_key).weather_at_place(location)

    def todays_forecast(self, location):
        return OWM(self.api_key).daily_forecast(location, limit=1)


class WeatherService(Service):

    def __init__(self, config=None, api=None):
        Service.__init__(self, config)

        api_key = 'b42dab02ba31304c08ae33bd9c63d0a4'

        if api is None:
            self._api = WeatherAPI(api_key)
        else:
            self._api = api

    def get_temp_info(self, observation):
        weather = observation.get_weather()
        return str(weather.get_temperature(unit='fahrenheit')['temp'])

    def get_forecast_info(self, forecaster):
        forecast = forecaster.get_forecast()
        return str(forecast)

    def get_status_info(self, observation):
        weather = observation.get_weather()
        # print(f"weather: {weather.get_status()}")
        if weather.get_status() == "Clouds":
            return "cloudy weather"
        elif weather.get_status() == "Clear":
            return "clear skies are"
        else:
            return str(weather.get_status()) + " is"

    def ask_question(self, client_context, question: str):
        try:
            words  = question.split()
            question = " ".join(words[1:])
            if words[0] == 'TEMPERATURE':
                search = requests.post('http://localhost:5000/api/rest/v1.0/weather',  json={'location': question}).text
                # observation = self._api.weather(question)
                # search = self.get_temp_info(observation)
                search += ' degrees fahrenheit'
                YLogger.debug(client_context, f"weather report: {search}")

            elif words[0] == "STATUS":
                observation = self._api.weather(question)
                search = self.get_status_info(observation)
            # NOTE: This API call doesn't work with free API subscriptions
            # elif words[0] == 'FORECAST':
            #     forecaster = self._api.todays_forecast(question)
            #     search = self.get_forecast_info(observation)

            else:
                YLogger.error(client_context, "Unknown Open Weather Map command [%s]", words[0])
                search = ""

            return search
        except Exception as ex:
            YLogger.error(client_context, "General error querying Open Weather Map for question [%s]", question)
            YLogger.error(client_context, f"Exception message: {ex}")
        return ""