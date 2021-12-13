# -*- coding: utf-8 -*-
from translators import model_translators


def actuatable_property_translator(actuatable_property_from_db):
    return {
        "id": actuatable_property_from_db.id,
        "name": actuatable_property_from_db.name,
        "feature_of_interest_name": actuatable_property_from_db.feature_of_interest_name,
    }


def actuation_translator(actuation_from_db):
    return {
        "id": actuation_from_db.id,
        "observation_id": actuation_from_db.observation_id,
        "context_awareness_rule_name": actuation_from_db.context_awareness_rule_name,
        "time_start": model_translators.translate_datetime(actuation_from_db.time_start),
        "time_end": model_translators.translate_datetime(actuation_from_db.time_end),
    }


def actuator_translator(actuator_from_db):
    return {
        "id": actuator_from_db.id,
        "thing_name": actuator_from_db.thing_name,
        "name": actuator_from_db.name,
        "actuatable_property_name": actuator_from_db.actuatable_property_name,
        "location_name": actuator_from_db.location_name,
    }


def context_awareness_rule_translator(context_awareness_rule_from_db):
    return {
        "id": context_awareness_rule_from_db.id,
        "name": context_awareness_rule_from_db.name,
        "sensor_observed_name": context_awareness_rule_from_db.sensor_observed_name,
        "operation_type": context_awareness_rule_from_db.operation_type.value,
        "executing": context_awareness_rule_from_db.executing,
        "priority": context_awareness_rule_from_db.priority,
        "value_to_compare_boolean": context_awareness_rule_from_db.value_to_compare_boolean,
        "value_to_compare_string": context_awareness_rule_from_db.value_to_compare_string,
        "value_to_compare_integer": context_awareness_rule_from_db.value_to_compare_integer,
        "value_to_compare_float": context_awareness_rule_from_db.value_to_compare_float,
    }


def feature_of_interest_translator(feature_of_interest_from_db):
    return {
        "id": feature_of_interest_from_db.id,
        "name": feature_of_interest_from_db.name,
        "location_name": feature_of_interest_from_db.location_name,
    }


def location_translator(location_from_db):
    return {
        "id": location_from_db.id,
        "name": location_from_db.name,
        "latlng": location_from_db.latlng,
    }


def observable_property_translator(observable_property_from_db):
    return {
        "id": observable_property_from_db.id,
        "name": observable_property_from_db.name,
        "value_type_to_measure": observable_property_from_db.value_type_to_measure.value,
        "feature_of_interest_name": observable_property_from_db.feature_of_interest_name,
    }


def observation_translator(observation_from_db):
    return {
        "id": observation_from_db.id,
        "sensor_name": observation_from_db.sensor_name,
        "time_start": model_translators.translate_datetime(observation_from_db.time_start),
        "time_end": model_translators.translate_datetime(observation_from_db.time_end),
        "value": observation_from_db.value,
    }


def platform_translator(platform_from_db):
    return {
        "id": platform_from_db.id,
        "name": platform_from_db.name,
        "location_name": platform_from_db.location_name,
    }


def sensor_translator(sensor_from_db):
    return {
        "id": sensor_from_db.id,
        "thing_name": sensor_from_db.thing_name,
        "name": sensor_from_db.name,
        "observable_property_name": sensor_from_db.observable_property_name,
        "location_name": sensor_from_db.location_name,
    }


def thing_translator(thing_from_db):
    return {
        "id": thing_from_db.id,
        "name": thing_from_db.name,
        "type_name": thing_from_db.type_name,
        "location_name": thing_from_db.location_name,
    }


def thing_type_translator(thing_type_from_db):
    return {
        "id": thing_type_from_db.id,
        "name": thing_type_from_db.name,
    }
