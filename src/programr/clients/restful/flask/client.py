import json
import datetime
from xmlrpc.client import ServerProxy

from flask import Flask, jsonify, request, make_response, abort, session, g
# import flask_login
# from werkzeug.contrib.profiler import ProfilerMiddleware

from programr.utils.logging.ylogger import YLogger
from programr.clients.restful.client import RestBotClient


# PROFILER = False

class FlaskRestBotClient(RestBotClient):

    def __init__(self, id, argument_parser=None):
        RestBotClient.__init__(self, id, argument_parser)
        self.initialise()

    def get_description(self):
        return 'ProgramR AIML2.0 Flask REST Client'

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.args or rest_request.args['apikey'] is None:
            return None
        return rest_request.args['apikey']

    def server_abort(self, error_code):
        abort(error_code)

    def get_question(self, rest_request):
        # YLogger.debug(self, f"In get_question, rest_request.data: {rest_request.data.decode('utf-8')}")
        # YLogger.debug(self, f"rest_request type: {type(rest_request)}")
        
        # TODO: Save userid to MongoDB with rest of user info
        rest_request = json.loads(rest_request.data.decode('utf-8'))

        # YLogger.debug(self, f"after json.loads, rest_request: {rest_request}")

        if "question" not in rest_request or rest_request["question"] is None:
            YLogger.error(self, "'question' missing from request")
            self.server_abort(400)
        return rest_request["question"]

    def get_userid(self, rest_request):
        rest_request = json.loads(rest_request.data.decode('utf-8'))
        if "userid" not in rest_request or rest_request['userid'] is None:
            YLogger.error(self, "'userid' missing from request")
            self.server_abort(400)
        return rest_request['userid']

    def create_response(self, response_data, status):
        if self.configuration.client_configuration.debug is True:
            self.dump_request(response_data)

        return make_response(jsonify({'response': response_data}, status))

    def run(self, flask):

        print("%s Client running on %s:%s" % (self.id, self.configuration.client_configuration.host,
                                              self.configuration.client_configuration.port))

        if self.configuration.client_configuration.debug is True:
            print("%s Client running in debug mode" % self.id)

        if self.configuration.client_configuration.ssl_cert_file is not None and \
                self.configuration.client_configuration.ssl_key_file is not None:
            context = (self.configuration.client_configuration.ssl_cert_file,
                       self.configuration.client_configuration.ssl_key_file)

            print("%s Client running in https mode" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      ssl_context=context)
        else:
            print("%s Client running in http mode, careful now !" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug)

    def dump_request(self, request):
        YLogger.debug(self, str(request))

# @app.before_request
# def before_request():
#     session.permanent = True
#     app.permanent_session_lifetime = datetime.timedelta(minutes=5)
#     session.modified = True
#     g.user = flask_login.current_user

# PORT = 5000
proxy = ServerProxy('http://localhost:3000')

if __name__ == '__main__':

    rest_client = None

    print("Initiating Flask REST Service...")
    app = Flask(__name__)


    @app.route('/api/rest/v1.0/ask', methods=['POST'])
    def ask():
        response_data, status = rest_client.process_request(request)
        return rest_client.create_response(response_data, status)

    @app.route('/api/rest/v1.0/wiki', methods=['POST'])
    def ask_wiki():
        r = request.get_json()
        response = make_response(jsonify({"response": proxy.wiki_summary(r["question"])}))
        return response

    @app.route('/api/rest/v1.0/sentiment', methods=['POST'])
    def ask_sentiment():
        r = request.get_json()
        response = make_response(jsonify({"response": proxy.check_sentiment(r["question"])}))
        return response

    @app.route('/api/rest/v1.0/similarity', methods=['POST'])
    def ask_similarity():
        r = request.get_json()
        response = make_response(jsonify({"response": proxy.get_semantic_similarity(r['text'], r['concept'])}))
        return response

    @app.route('/api/rest/v1.0/news', methods=['POST'])
    def ask_news():
        r = request.get_json()
        response = make_response(jsonify({"response": proxy.get_news(r['headline_index'])}))
        return response

    @app.route('/api/rest/v1.0/weather_temperature', methods=['POST'])
    def ask_weather_temperature():
        r = request.get_json()
        response = make_response(jsonify({"response": proxy.get_weather_temperature(r['location'])}))
        return response

    @app.route('/api/rest/v1.0/weather_status', methods=['POST'])
    def ask_weather_status():
        r = request.get_json()
        response = make_response(jsonify({"response": proxy.get_weather_status(r['location'])}))
        return response

    

    print("Loading, please wait...")
    rest_client = FlaskRestBotClient("flask")
    rest_client.run(app)


#curl --header "Content-Type: application/json" --request POST --data '{"question":"hellooo","userid":123456}' http://localhost:5000/api/rest/v1.0/ask