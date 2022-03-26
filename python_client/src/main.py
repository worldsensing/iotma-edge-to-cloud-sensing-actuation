import time
from threading import Thread

import schedule
from flask import Flask

from __init__ import SENSOR_CONFIGURED, ACTUATOR_CONFIGURED
from api import api
from connector_grovepi import pin_mode, send_digital_value
from context_awareness import get_context_awareness_rules, read_sensor_information
from socketio_events import SocketIOEvents

app = Flask(__name__)
app.register_blueprint(api)

if SENSOR_CONFIGURED == "LIGHT":
    LIGHT_SENSOR = 1  # Analog port 1
    RED_LED = 2  # Digital port 2
    RED_LED_THRESHOLD = 100

    pin_mode(RED_LED, "OUTPUT")
    send_digital_value(RED_LED, 0)

if ACTUATOR_CONFIGURED == "BUZZER":
    GREEN_LED = 2  # Digital port 2
    send_digital_value(GREEN_LED, 0)
    BUZZER_PIN = 3  # Digital port 3
    send_digital_value(BUZZER_PIN, 0)
    BLUE_LED = 4  # Digital port 4
    send_digital_value(BLUE_LED, 0)


def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    print("Starting up code...")

    if SENSOR_CONFIGURED == "LIGHT":
        print("Setup Scheduler...")
        get_context_awareness_rules()
        read_sensor_information()

        schedule.every(5).seconds.do(get_context_awareness_rules)
        schedule.every(3).seconds.do(read_sensor_information)

        t = Thread(target=run_schedule)
        t.start()

    print("Setup SocketIO...")
    socketio = SocketIOEvents("http://35.195.86.253:5001")
    time.sleep(1)

    print("Setup Flask server...")
    app.run(host="0.0.0.0", port=8001, use_reloader=False)
