import signal
import sys
import time

import socketio

import actuation
from __init__ import PC_MODE


class SocketIOEvents:
    socketIO = socketio.Client(ssl_verify=False)

    @staticmethod
    @socketIO.on("/on_connect_checks")
    def on_connect_checks():
        print("Received: on_connect_checks")

    @staticmethod
    @socketIO.on("/on_receive_actuation_info")
    def on_receive_actuation_info(args):
        print(f"Received: on_receive_actuation_info: {args}")

        alarm_trigger = bool(args["trigger"])
        actuation_id = int(args["origin_actuation"])
        actuation.trigger_actuation(alarm_trigger, actuation_id, "NORMAL_LATENCY")

    def send_actuation_info(self, actuation_trigger, actuation_id):
        event_to_emit = "/on_receive_actuation_info"
        print(f"Send: /forward_message_to_clients: {event_to_emit} {actuation_trigger}")

        self.socketIO.emit("/forward_message_to_clients", data={
            "event_name": event_to_emit,
            "data": {
                "trigger": actuation_trigger,
                "origin_actuation": actuation_id
            }
        })

    def signal_handler(self, sig, frame):
        print("Stopping script...")

        if PC_MODE:  # Debug purposes
            self.send_actuation_info(True)
        else:
            self.socketIO.disconnect()
            time.sleep(1)
            sys.exit(0)

    def __init__(self, url="localhost:5001") -> None:
        super().__init__()

        self.url = url

    def connect(self):
        self.socketIO.connect(self.url)
        signal.signal(signal.SIGINT, self.signal_handler)

        self.socketIO.emit("/connect")
