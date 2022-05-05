import json

import requests

import utils
from __init__ import URL_POST_ACTUATION_CLOUD

BASE_URL = URL_POST_ACTUATION_CLOUD
CONTEXT_AWARENESS_ENDPOINT_URL = "/context-awareness-rules/"
SENSORS_ENDPOINT_URL = "/sensors/"
SENSOR_OBSERVATIONS_ENDPOINT_URL = "/observations/"  # TODO Change to /sensor-observations/
OBSERVATIONS_ENDPOINT_URL = "/observations/"
OBSERVABLE_PROPERTIES_ENDPOINT_URL = "/observable-properties/"
ACTUATIONS_ENDPOINT_URL = "/actuations/"


def context_awareness_rule_should_be_triggered_observation(
        context_awareness_rule, observable_property, sensor_observations):
    operation_type = context_awareness_rule["operation_type"]
    value_type_to_measure = observable_property["value_type_to_measure"]

    value_to_compare = utils.get_value_to_compare_from_context_awareness_rule(
        context_awareness_rule)

    raise_trigger = False
    for sensor_observation in sensor_observations:
        observation_value = sensor_observation["value"]

        if operation_type == "EQUAL":
            raise_trigger = value_to_compare == observation_value
        elif operation_type == "NOT_EQUAL":
            raise_trigger = value_to_compare != observation_value
        elif operation_type == "LESS_THAN":
            raise_trigger = value_to_compare > observation_value
        elif operation_type == "MORE_THAN":
            raise_trigger = value_to_compare < observation_value

        if raise_trigger:
            return sensor_observation

    return None


def get_observation(observation):
    print(f"Sending GET to obtain Observation data {observation}...")
    url = f"{BASE_URL}{OBSERVATIONS_ENDPOINT_URL}{observation}/"
    print(url)

    r = requests.get(url)
    observation = json.loads(r.content)["data"]
    print(observation)

    return observation


def get_observable_property(observable_property_name):
    print(
        f"Sending GET to obtain ObservableProperty data for ObservableProperty {observable_property_name}...")
    url = f"{BASE_URL}{OBSERVABLE_PROPERTIES_ENDPOINT_URL}{observable_property_name}/"
    print(url)

    r = requests.get(url)
    observable_property = json.loads(r.content)["data"]
    print(observable_property)

    return observable_property


def get_sensor(sensor_name):
    print(f"Sending GET to obtain Sensor data for Sensor {sensor_name}...")
    url = f"{BASE_URL}{SENSORS_ENDPOINT_URL}{sensor_name}/"
    print(url)

    r = requests.get(url)
    sensor = json.loads(r.content)["data"]
    print(sensor)

    return sensor


def post_sensor_observation(value):
    print(f"Sending POST to create an observation")
    url = f"{BASE_URL}{OBSERVATIONS_ENDPOINT_URL}"
    print(url)
    body = {"sensor_name": "RainSensor", "time_start": utils.get_current_time(), "value": value}
    print(body)

    r = requests.post(url, json=body)
    observation = json.loads(r.content)["data"]
    print(observation)

    return observation["id"]


def get_sensor_observations(sensor_name):
    print(f"Sending GET to obtain Observation data for Sensor {sensor_name}...")
    url = f"{BASE_URL}{SENSOR_OBSERVATIONS_ENDPOINT_URL}"
    print(url)

    r = requests.get(url)
    all_sensor_observations = json.loads(r.content)["data"]
    print(all_sensor_observations)

    sensor_observations = []
    # Temporal code to remove the non-wanted sensors
    for sensor_observation in all_sensor_observations:
        if sensor_observation["sensor_name"] == sensor_name:
            sensor_observations.append(sensor_observation)

    print("Real Sensor Observations...")
    print(sensor_observations)

    return sensor_observations


def get_actuation(actuation_id):
    print(f"Sending GET to obtain Actuation for Actuation {actuation_id} ")
    url = f"{BASE_URL}{ACTUATIONS_ENDPOINT_URL}{actuation_id}/"
    print(url)

    r = requests.get(url)
    actuation = json.loads(r.content)["data"]
    print(actuation)

    return actuation


def create_actuation(observation_id, context_awareness_rule_name):
    print(f"Sending POST to create an Actuation for ObservationID {observation_id} "
          f"and ContextAwarenessRuleName {context_awareness_rule_name}...")
    url = f"{BASE_URL}{ACTUATIONS_ENDPOINT_URL}"
    print(url)

    body = {
        "observation_id": observation_id,
        "context_awareness_rule_name": context_awareness_rule_name,
        "time_start": None,
        "time_end": None
    }
    print(body)

    r = requests.post(url, json=body)
    actuation = json.loads(r.content)["data"]
    print(actuation)

    return actuation["id"]


def patch_actuation_start_time(actuation_id, actuation_start_time):
    print(f"Sending PATCH to update START_TIME of an Actuation for Actuation ID {actuation_id} ")
    url = f"{BASE_URL}{ACTUATIONS_ENDPOINT_URL}{actuation_id}/"
    print(url)

    body = {
        "time_start": actuation_start_time,
    }
    print(body)

    r = requests.patch(url, json=body)
    print(r.text)
    actuation_id = json.loads(r.content)["data"]
    print(actuation_id)


def patch_actuation_end_time(actuation_id, actuation_end_time):
    print(f"Sending PATCH to update END_TIME of an Actuation for Actuation ID {actuation_id} ")
    url = f"{BASE_URL}{ACTUATIONS_ENDPOINT_URL}{actuation_id}/"
    print(url)

    body = {
        "time_end": actuation_end_time,
    }
    print(body)

    r = requests.patch(url, json=body)
    print(r.text)
    actuation_id = json.loads(r.content)["data"]
    print(actuation_id)


def get_context_awareness_rules():
    print("Sending GET to obtain Context Awareness Rules...")
    url = f"{BASE_URL}{CONTEXT_AWARENESS_ENDPOINT_URL}"
    print(url)

    r = requests.get(url)
    context_awareness_rules = json.loads(r.content)["data"]
    print(context_awareness_rules)

    return context_awareness_rules
