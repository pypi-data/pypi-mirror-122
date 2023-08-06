import json
import logging
import time
from threading import Timer

from paho.mqtt import client as mqtt_client

import yaml


logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="[%H:%M:%S]", level=logging.DEBUG
)


class RepeatTimer:
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()


class BasicDyrkDevice:
    def __init__(self) -> None:
        self.EVENTS = dict()
        self.MEASURES = dict()
        self.EVENTPARSERS = dict()

        self.EVENTPARSERS["enroll_event"] = self.enrollEventParser
        self.EVENTPARSERS["output_event"] = self.outputEventParser
        self.EVENTPARSERS["data_event"] = self.dataEventParser

        self.EVENTS["enroll_event"] = self.subscribe_to_topic

        with open("deviceconfig.yml", "r") as ymlfile:
            self.device_config = yaml.safe_load(ymlfile)

    def connect_mqtt(self):
        broker = self.device_config["mqtt"]["broker"]["endpoint"]
        port = self.device_config["mqtt"]["broker"]["port"]
        # generate client ID with pub prefix randomly
        client_id = self.device_config["mqtt"]["broker"]["client_id"]
        username = self.device_config["mqtt"]["broker"]["username"]
        password = self.device_config["mqtt"]["broker"]["password"]

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Connected to MQTT Broker!")
            else:
                logging.info("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        client = mqtt_client.Client(client_id)
        client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(broker, port)

        return client

    def subscribe_to_topic(self, topic):
        logging.info(f"Subscribing to topic: {topic}")

        def on_message(client, userdata, msg):
            try:
                eventstring = msg.payload.decode()
                parsedevent = json.loads(eventstring)
                logging.info(f"[{msg.topic}] Received an event: {parsedevent}")
                if parsedevent["event_type"] not in self.EVENTS.keys():
                    logging.info("Event unsupported")
                    return

                self.EVENTS[parsedevent["event_type"]](
                    self.EVENTPARSERS[parsedevent["event_type"]](parsedevent)
                )

            except ValueError:
                logging.info("String could not be converted to JSON.")

        self.client.subscribe(topic)
        self.client.on_message = on_message

    def outputEventParser(self, event: dict):
        return event["output_amount"]

    def enrollEventParser(self, event: dict):
        return event["plan_id"]

    def dataEventParser(self, event: dict):
        return

    def event(self, eventName: str):
        def eventdecorator(func):
            self.EVENTS[eventName] = func
            return func

        return eventdecorator

    def eventParser(self, eventName: str):
        def parserdecorator(func):
            self.EVENTPARSERS[eventName] = func
            return func

        return parserdecorator

    def measure(self, measureName: str, interval: int):
        def decorator(func):
            def send_dict():
                data = func()

                data["event_type"] = "data_event"
                data["timestamp"] = int(time.time())

                eventstring = json.dumps(data)
                self.client.publish(self.data_channel_id, eventstring)

            timer = RepeatTimer(interval, send_dict)
            self.MEASURES[measureName] = timer
            return timer

        return decorator

    def run(self):
        self.command_channel_id = (
            self.device_config["mqtt"]["broker"]["client_id"] + "_command"
        )
        self.data_channel_id = (
            self.device_config["mqtt"]["broker"]["client_id"] + "_data"
        )

        self.client = self.connect_mqtt()
        self.subscribe_to_topic(self.command_channel_id)
        self.subscribe_to_topic(self.data_channel_id)

        for name, thread in self.MEASURES.items():
            thread.start()
            logging.info(f"started {name}")

        self.client.loop_start()
        while True:
            pass
