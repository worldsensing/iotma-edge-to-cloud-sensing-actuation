import signal
import sys
import time

import socketio

import actuation


class SocketIOEvents:
    socketIO = socketio.Client()

    @staticmethod
    @socketIO.on("/on_connect_checks")
    def on_connect_checks():
        print("Received: on_connect_checks")

    @staticmethod
    @socketIO.on("/on_receive_actuation_info")
    def on_receive_actuation_info(args):
        print(f"Received: on_receive_actuation_info: {args}")
        json_received = args["data"]

        alarm_trigger = bool(json_received["trigger"])
        actuation.trigger_actuation(alarm_trigger)

    def send_actuation_info(self, actuation_trigger):
        print(f"Send: send_actuation_info: {actuation_trigger}")

        self.socketIO.emit("/on_receive_actuation_info", {"data": {"trigger": actuation_trigger}})

    def signal_handler(self, sig, frame):
        print("Stopping script...")
        self.socketIO.disconnect()
        time.sleep(1)
        sys.exit(0)

    def __init__(self, url="localhost:5001") -> None:
        super().__init__()

        self.socketIO.connect(url)
        signal.signal(signal.SIGINT, self.signal_handler)

        self.socketIO.emit("/connect")
