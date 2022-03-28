import json
import time

import requests

import connector_grovepi
from __init__ import IOTMA_SENSOR_NAME, URL_POST_ACTUATION_EDGE
from core import get_context_awareness_rules as get_ca_rules_core, get_sensor, \
    get_observable_property, get_observation, create_actuation, \
    context_awareness_rule_should_be_triggered_observation
from utils import get_current_time

context_awareness_rules = None


def get_context_awareness_rules():
    global context_awareness_rules
    context_awareness_rules = get_ca_rules_core()


def check_context_awareness_rules(sensor_observation_id):
    global context_awareness_rules

    if context_awareness_rules is not None:
        for context_awareness_rule in context_awareness_rules:
            if context_awareness_rule["executing"]:
                print(context_awareness_rule)
                sensor_name = context_awareness_rule["sensor_observed_name"]

                if sensor_name == IOTMA_SENSOR_NAME:
                    sensor = get_sensor(sensor_name)
                    observable_property = get_observable_property(
                        sensor["observable_property_name"])
                    # This should be used
                    # sensor_observations = get_sensor_observations(sensor_name)
                    # This line is temporal
                    sensor_observations = [get_observation(sensor_observation_id)]

                    observation_triggered = context_awareness_rule_should_be_triggered_observation(
                        context_awareness_rule, observable_property, sensor_observations)

                    if observation_triggered is not None:
                        create_actuation(observation_triggered, context_awareness_rule)
                        return context_awareness_rule["priority"]
    return None


def read_sensor_information():
    from main import LIGHT_SENSOR, RED_LED

    try:
        resistance_value = connector_grovepi.read_analog_value(LIGHT_SENSOR)
        print(f"Value is: {resistance_value}")
        observation_id = send_post_for_observation(resistance_value)

        connector_grovepi.send_digital_value(RED_LED, 0)
        time.sleep(1)
        should_raise_priority_actuation = check_context_awareness_rules(observation_id)

        if should_raise_priority_actuation is not None and should_raise_priority_actuation:
            print("Raise priority actuation")
            send_high_priority_actuation()
        else:
            send_normal_priority_actuation()

    except IOError as error:
        print("Error")
        print(error)


def send_post_for_observation(value):
    from core import BASE_URL, OBSERVATIONS_ENDPOINT_URL
    print(f"post_observation")
    body = {"sensor_name": "RainSensor", "time_start": get_current_time(), "value": value}
    print(body)
    r = requests.post(url=f"{BASE_URL}{OBSERVATIONS_ENDPOINT_URL}", json=body)

    observation = json.loads(r.content)["data"]
    return observation["id"]


def send_high_priority_actuation():
    from main import RED_LED

    connector_grovepi.send_digital_value(RED_LED, 1)
    requests.post(url=f"{URL_POST_ACTUATION_EDGE}/actuation", json={"trigger": True})


def send_normal_priority_actuation():
    from main import RED_LED, socketio

    connector_grovepi.send_digital_value(RED_LED, 1)
    socketio.send_actuation_info(True)
