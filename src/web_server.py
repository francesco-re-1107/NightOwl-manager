from flask import Flask
from waitress import serve
import sys
from utils import get_logger
import json

LOGGER = get_logger()

class WebServer:
    def __init__(self, analyzer):   
        self.__analyzer = analyzer     
        self.__app = Flask(__name__)
        self.__app.add_url_rule("/start_trigger", "start_trigger", self.start_trigger)
        self.__app.add_url_rule("/end_trigger", "end_trigger", self.end_trigger)
        self.__app.add_url_rule("/trigger_datetimes", "trigger_datetimes", self.trigger_datetimes)

    def start_trigger(self):
        LOGGER.info("Starting trigger")
        self.__analyzer.start()
        return "OK"

    def end_trigger(self):
        LOGGER.info("Ending trigger")
        self.__analyzer.end()
        return "OK"

    def trigger_datetimes(self):
        return json.dumps(self.__analyzer.trigger_datetimes)

    def start(self):
        try:
            LOGGER.info("Starting web server")
            serve(self.__app, host="0.0.0.0", port=7070)
        except Exception as e:
            print(e)
            sys.exit(1)