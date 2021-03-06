from programr.utils.logging.ylogger import YLogger
import socket
import json

from programr.clients.events.client import EventBotClient
from programr.clients.events.tcpsocket.config import SocketConfiguration
from programr.clients.render.json import JSONRenderer
from programr.services.service import ServiceFactory

class ClientConnection(object):

    def __init__(self, clientsocket, addr, max_buffer):
        self._clientsocket = clientsocket
        self._addr = addr
        self._max_buffer = max_buffer

    def receive_data(self):
        json_data = self._clientsocket.recv(self._max_buffer).decode()
        YLogger.debug(self, "Received: %s", json_data)
        return json.loads(json_data, encoding="utf-8")

    def send_response(self, userid, answer):
        return_payload = {"result": {"status": "OK", "userid": userid}, "answer": answer}
        json_data = json.dumps(return_payload)

        YLogger.debug(self, "Sent %s:", json_data)

        self._clientsocket.send(json_data.encode('utf-8'))

    def send_error(self, error):
        if hasattr(error, 'message') is True:
            return_payload = {"result": {"status":"ERROR", "message": error.message}}
        elif hasattr(error, 'msg') is True:
            return_payload = {"result": {"status": "ERROR", "message": error.msg}}
        else:
            return_payload = {"result": {"status": "ERROR", "message": str(error)}}

        json_data = json.dumps(return_payload)

        YLogger.debug(self, "Sent: %s", json_data)

        self._clientsocket.send(json_data.encode('utf-8'))

    def close(self):
        if self._clientsocket is not None:
            self._clientsocket.close()
            self._clientsocket = None


class SocketFactory(object):

    def create_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM):
        return socket.socket(family, type)


class SocketConnection(object):
    
    def __init__(self, host, port, queue, max_buffer=1024, factory=SocketFactory()):
        self._socket_connection = self._create_socket(host, port, queue, factory)
        self._max_buffer = max_buffer

    def _create_socket(self, host, port, queue, factory):
        # create a socket object
        serversocket = factory.create_socket()
        # bind to the port
        serversocket.bind((host, port))
        # queue up to 5 requests
        serversocket.listen(queue)
        return serversocket

    def accept_connection(self):
        # establish a connection
        clientsocket, addr = self._socket_connection.accept()
        return ClientConnection(clientsocket, addr, self._max_buffer )


class SocketBotClient(EventBotClient):

    def __init__(self, argument_parser=None):
        EventBotClient.__init__(self, "Socket", argument_parser)

        print("TCP Socket Client server now listening on %s:%d"%(self._host, self._port))
        self._server_socket = self.create_socket_connection(self._host, self._port, self._queue, self._max_buffer)

        self._renderer = JSONRenderer(self)

        config = self.client_context.brain.configuration
        self.client_context.brain.load_services(config)



    def get_description(self):
        return 'ProgramR AIML2.0 TCP Socket Client'

    def get_client_configuration(self):
        return SocketConfiguration()

    def parse_configuration(self):
        self._host = self.configuration.client_configuration.host
        self._port = self.configuration.client_configuration.port
        self._queue = self.configuration.client_configuration.queue
        self._max_buffer = self.configuration.client_configuration.max_buffer

    def extract_question(self, receive_payload):
        question = None
        if 'question' in receive_payload:
            question = receive_payload['question']
        if question is None or question == "":
            raise Exception("Clientid missing from payload")
        return question

    def extract_userid(self, receive_payload):
        userid = None
        if 'userid' in receive_payload:
            userid = receive_payload['userid']
        if userid is None or userid == "":
            raise Exception("Clientid missing from payload")
        return userid

    def extract_servicename(self, receive_payload):
        servicename = None
        if 'servicename' in receive_payload:
            servicename = receive_payload['servicename']
        if servicename is None or servicename == "":
            raise Exception("servicename missing from payload")
        return servicename

    def ask_question_from_service(self, servicename, question):
        service = ServiceFactory.get_service(servicename)
        answer = service.ask_question(self.client_context, question)
        return answer


    def create_socket_connection(self, host, port, queue, max_buffer):
        return SocketConnection(host, port, queue, max_buffer)

    def process_question(self, client_context, question):
        # Returns a response
        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def render_response(self, client_context, response):
        # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        self._client_connection.send_response(client_context.userid, response)


    def run_loop(self):
        bot = self.bot_factory.bot("bot")
        self._running = True
        bot.initiate_conversation_storage()

        while self._running:
            self._running = self.wait_and_answer()


    def wait_and_answer(self,):
        running = True
        try:
            self._client_connection = self._server_socket.accept_connection()

            receive_payload = self._client_connection.receive_data()

            question = self.extract_question(receive_payload)
            userid = self.extract_userid(receive_payload)
            service_name = self.extract_servicename(receive_payload)

            client_context = self.create_client_context(userid)

            answer = self.ask_question_from_service(service_name, question)

            self.render_response(client_context, answer)

        except KeyboardInterrupt:
            running = False
            YLogger.debug(self, "Cleaning up and exiting...")

        except Exception as e:
            if self._client_connection is not None:
                self._client_connection.send_error(e)

        finally:
            if self._client_connection is not None:
                self._client_connection.close()

        return running


    def run(self):
        if self.arguments.noloop is False:
            YLogger.info(self, "Entering conversation loop...")

            self.prior_to_run_loop()

            self.run_loop()

            self.post_run_loop()

        else:
            YLogger.debug(self, "noloop set to True, exiting...")


if __name__ == '__main__':

    def run():
        print("Loading, please wait...")
        console_app = SocketBotClient()
        console_app.run()

    run()


