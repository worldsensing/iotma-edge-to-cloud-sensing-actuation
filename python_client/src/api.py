from flask import request, Blueprint

import actuation

api = Blueprint("api", __name__)


@api.route("/actuation", methods=["POST"])
def post():
    resp_json = request.json

    alarm_trigger = bool(resp_json["trigger"])

    actuation.trigger_actuation(alarm_trigger, "LOW_LATENCY")

    return "OK"
