import signal
import sys
import time

from socketIO_client import SocketIO


class SocketIOEvents:

    @staticmethod
    def on_connect_checks():
        print("Received: on_connect_checks")

    def signal_handler(self, sig, frame):
        print("Stopping script...")
        self.socketIO.disconnect()
        time.sleep(1)
        sys.exit(0)

    def __init__(self, address="localhost", port="5001") -> None:
        super().__init__()

        self.socketIO = SocketIO(address, port)
        signal.signal(signal.SIGINT, self.signal_handler)
        self.socketIO.wait(seconds=1)

        self.socketIO.on("/on_connect_checks", self.on_connect_checks)

        self.socketIO.emit("/connect")

        self.socketIO.wait(seconds=1)
