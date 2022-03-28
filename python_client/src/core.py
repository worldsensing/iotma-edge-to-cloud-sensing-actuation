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
    print(r.text)
    observable_property = json.loads(r.content)["data"]

    return observable_property


def get_sensor(sensor_name):
    print(f"Sending GET to obtain Sensor data for Sensor {sensor_name}...")
    url = f"{BASE_URL}{SENSORS_ENDPOINT_URL}{sensor_name}/"
    print(url)

    r = requests.get(url)
    print(r.text)
    sensor = json.loads(r.content)["data"]

    return sensor


def get_sensor_observations(sensor_name):
    print(f"Sending GET to obtain Observation data for Sensor {sensor_name}...")
    url = BASE_URL + SENSOR_OBSERVATIONS_ENDPOINT_URL
    print(url)

    r = requests.get(url)
    print(r.text)
    all_sensor_observations = json.loads(r.content)["data"]

    sensor_observations = []
    # Temporal code to remove the non-wanted sensors
    for sensor_observation in all_sensor_observations:
        if sensor_observation["sensor_name"] == sensor_name:
            sensor_observations.append(sensor_observation)

    print("Real Sensor Observations...")
    print(sensor_observations)

    return sensor_observations


def create_actuation(observation, context_awareness_rule):
    print(f"Sending POST to create an Actuation for ObservationID {observation['id']} "
          f"and ContextAwarenessRuleName {context_awareness_rule['name']}...")
    url = BASE_URL + ACTUATIONS_ENDPOINT_URL
    print(url)

    data = {
        "observation_id": observation["id"],
        "context_awareness_rule_name": context_awareness_rule["name"],
        "time_start": utils.get_current_time(),
        "time_end": None
    }

    r = requests.post(url, json=data)
    print(r.text)


def get_context_awareness_rules():
    print("Sending GET to obtain Context Awareness Rules...")
    url = BASE_URL + CONTEXT_AWARENESS_ENDPOINT_URL
    print(url)

    r = requests.get(url)
    context_awareness_rules = json.loads(r.content)["data"]
    print(context_awareness_rules)

    return context_awareness_rules
