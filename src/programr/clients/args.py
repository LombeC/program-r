import logging
import argparse


class ClientArguments(object):

    def __init__(self, client, parser=None):
        self._bot_root = "."
        self._logging = logging.DEBUG
        self._config_name = "config.yaml"
        self._config_format = "yaml"
        self._no_loop = False

    def parse_args(self, client):
        pass

    @property
    def bot_root(self):
        return self._bot_root

    @bot_root.setter
    def bot_root(self, root):
        self._bot_root = root

    @property
    def logging(self):
        return self._logging

    @property
    def config_filename(self):
        return self._config_name

    @property
    def config_format(self):
        return self._config_format

    @property
    def noloop(self):
        return self._no_loop


class CommandLineClientArguments(ClientArguments):

    def __init__(self, client, parser=None):
        self.args = None
        self._bot_root = None
        self._logging = None
        self._config_name = None
        self._config_format = None
        self._no_loop = False

        super().__init__(client)
        if parser is None:
            self.parser = argparse.ArgumentParser(description=client.get_description())
        else:
            self.parser = parser
        self.parser.add_argument('--bot_root', dest='bot_root', help='root folder for all bot configuration data')
        self.parser.add_argument('--config', dest='config', help='configuration file location')
        self.parser.add_argument('--cformat', dest='cformat', help='configuration file format (yaml|json|ini)')
        self.parser.add_argument('--logging', dest='logging', help='logging configuration file')
        self.parser.add_argument('--noloop', dest='noloop', action='store_true', help='do not enter conversation loop')
        client.add_client_arguments(self.parser)

    def parse_args(self, client):
        self.args = self.parser.parse_args()
        self._bot_root = self.args.bot_root
        self._logging = self.args.logging
        self._config_name = self.args.config
        self._config_format = self.args.cformat
        self._no_loop = self.args.noloop
        client.parse_args(self, self.args)
