from flask_socketio import emit

from app import socketio, logger


@socketio.on("/connect")
def test_connect():
    logger.info("Client connected")
    emit("/on_connect_checks")


# This route cannot be changed as the socket-io-client implements "disconnect" as callback
@socketio.on("disconnect")
def test_disconnect():
    logger.info("Client disconnected")


@socketio.on("/receive_alarm_to_emit")
def receive_alarm_to_emit():
    emit("/on_receive_actuation_info", {
        "data": {
            "trigger": "WelcomePEPE"
        }
    })
