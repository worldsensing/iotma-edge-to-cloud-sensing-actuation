import requests

import connector_grovepi
import utils
from __init__ import IOTMA_SENSOR_NAME, URL_POST_ACTUATION_EDGE
from core import get_context_awareness_rules as get_ca_rules_core, get_sensor, \
    get_observable_property, get_observation, create_actuation, \
    context_awareness_rule_should_be_triggered_observation, post_sensor_observation, \
    patch_actuation_start_time

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
                        return context_awareness_rule
    return None


def read_sensor_information():
    from main import LIGHT_SENSOR, RED_LED

    try:
        resistance_value = connector_grovepi.read_analog_value(LIGHT_SENSOR)
        print(f"Value is: {resistance_value}")
        observation_id = post_sensor_observation(resistance_value)

        connector_grovepi.send_digital_value(RED_LED, 0)
        context_awareness_rule = check_context_awareness_rules(observation_id)

        if context_awareness_rule is not None:
            actuation_id = create_actuation(observation_id, context_awareness_rule['name'])

            actuation_start_time = utils.get_current_time()
            if context_awareness_rule["priority"]:
                send_high_priority_actuation(actuation_id)
            else:
                send_normal_priority_actuation(actuation_id)

            patch_actuation_start_time(actuation_id, actuation_start_time)
    except IOError as error:
        print("Error")
        print(error)


def send_high_priority_actuation(actuation_id):
    from main import RED_LED

    print("Raise HIGH PRIORITY actuation")

    connector_grovepi.send_digital_value(RED_LED, 1)
    requests.post(url=f"{URL_POST_ACTUATION_EDGE}/actuation",
                  json={"trigger": True,
                        "origin_actuation": actuation_id})


def send_normal_priority_actuation(actuation_id):
    from main import RED_LED, socketio

    print("Raise NORMAL PRIORITY actuation")

    connector_grovepi.send_digital_value(RED_LED, 1)
    socketio.send_actuation_info(True, actuation_id)
