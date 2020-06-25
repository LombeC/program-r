from programr.utils.logging.ylogger import YLogger

from programr.oob.oob import OutOfBandProcessor


class AlarmOutOfBandProcessor(OutOfBandProcessor):
    """
    <oob>
        <alarm><message><star/></message><get name="sraix"/></alarm>
    </oob>

    <oob>
        <alarm><hour>11</hour><minute>30</minute></alarm>
    </oob>
    """

    def __init__(self):
        super().__init__()
        self._hour = None
        self._min = None
        self._message = None

    def parse_oob_xml(self, oob):
        if oob is not None:
            for child in oob:
                if child.tag == 'hour':
                    self._hour = child.text
                elif child.tag == 'minute':
                    self._min = child.text
                elif child.tag == 'message':
                    self._message = child.text
                else:
                    YLogger.error(self, "Unknown child element [%s] in alarm oob", child.tag)

            if self._hour is not None and self._min is not None:
                return True
            if self._message is not None:
                return True

        YLogger.error(self, "Invalid alarm oob command, either hour,min or message ")
        return False

    def execute_oob_command(self, client_context):
        if self._message is not None:
            YLogger.info(client_context, "AlarmOutOfBandProcessor: Showing alarm=%s", self._message)
        elif self._hour is not None and self._min is not None:
            YLogger.info(client_context, "AlarmOutOfBandProcessor: Setting alarm for %s:%s", self._hour, self._min)
        return "ALARM"
