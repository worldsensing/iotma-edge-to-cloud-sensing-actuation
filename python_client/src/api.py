from flask import request, Blueprint

import actuation

api = Blueprint("api", __name__)


@api.route("/actuation", methods=["POST"])
def post():
    resp_json = request.json

    alarm_trigger = bool(resp_json["trigger"])
    actuation_id = int(resp_json["origin_actuation"])
    actuation.trigger_actuation(alarm_trigger, actuation_id, "LOW_LATENCY")

    return "OK"
