import json

import pytest

from fixtures import ContextAwarenessRuleFactory2DB, ContextAwarenessRuleDictFactory, \
    ThingTypeFactory2DB, ThingFactory2DB, SensorFactory2DB
from models import ContextAwarenessRule
from models.ContextAwarenessRule import ContextAwarenessOperationEnum


def assert_context_awareness_rules(context_awareness_rule_api, context_awareness_rule_db):
    # assert context_awareness_rule_db["id"] == context_awareness_rule_api["id"]
    assert context_awareness_rule_db["name"] == context_awareness_rule_api["name"]
    assert context_awareness_rule_db["sensor_observed_name"] == \
           context_awareness_rule_api["sensor_observed_name"]
    if type(context_awareness_rule_db["operation_type"]) == ContextAwarenessOperationEnum:
        assert context_awareness_rule_db["operation_type"].value == \
               context_awareness_rule_api["operation_type"]
    else:
        assert context_awareness_rule_db["operation_type"] == \
               context_awareness_rule_api["operation_type"]
    assert context_awareness_rule_db["executing"] == context_awareness_rule_api["executing"]
    assert context_awareness_rule_db["priority"] == context_awareness_rule_api["priority"]
    assert context_awareness_rule_db["value_to_compare_boolean"] == \
           context_awareness_rule_api["value_to_compare_boolean"]
    assert context_awareness_rule_db["value_to_compare_string"] == \
           context_awareness_rule_api["value_to_compare_string"]
    assert context_awareness_rule_db["value_to_compare_integer"] == \
           context_awareness_rule_api["value_to_compare_integer"]
    assert context_awareness_rule_db["value_to_compare_float"] == \
           context_awareness_rule_api["value_to_compare_float"]


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="ABC-1001", type_name="Inclinometer")


@pytest.fixture
def create_sensor_2(create_thing):
    return SensorFactory2DB(thing_name="ABC-1001", name="Sensor2")


@pytest.fixture
def create_sensor(create_thing):
    return SensorFactory2DB(thing_name="ABC-1001", name="Sensor1")


@pytest.mark.parametrize("test_input, test_input_2", [
    (["Rule1", "Sensor1", "NOT_EQUAL", True, True, True],
     ["Rule2", "Sensor2", "LESS_THAN", True, 1])
])
def test_get_context_awareness_rules_all(api_client, orm_client, create_sensor, create_sensor_2,
                                         test_input, test_input_2):
    assert orm_client.session.query(ContextAwarenessRule).count() == 0
    context_awareness_rule_1 = ContextAwarenessRuleFactory2DB(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=ContextAwarenessOperationEnum(test_input[2]),
        executing=test_input[3],
        priority=test_input[4],
        value_to_compare_boolean=test_input[5])
    assert orm_client.session.query(ContextAwarenessRule).count() == 1
    context_awareness_rule_2 = ContextAwarenessRuleFactory2DB(
        name=test_input_2[0],
        sensor_observed_name=test_input_2[1],
        operation_type=ContextAwarenessOperationEnum(test_input_2[2]),
        executing=test_input_2[3],
        value_to_compare_boolean=test_input_2[4])
    assert orm_client.session.query(ContextAwarenessRule).count() == 2

    rv = api_client.get(f"/context-awareness-rules/")
    assert rv.status_code == 200
    response_content_1 = json.loads(rv.data)['data'][0]
    response_content_2 = json.loads(rv.data)['data'][1]
    assert_context_awareness_rules(response_content_1, context_awareness_rule_1.__dict__)
    assert_context_awareness_rules(response_content_2, context_awareness_rule_2.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Rule1", "Sensor1", "NOT_EQUAL", True, True])
])
def test_get_context_awareness_rule(api_client, orm_client, create_sensor,
                                    test_input):
    assert orm_client.session.query(ContextAwarenessRule).count() == 0
    context_awareness_rule_1 = ContextAwarenessRuleFactory2DB(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=ContextAwarenessOperationEnum(test_input[2]),
        executing=test_input[3],
        value_to_compare_boolean=test_input[4])
    assert orm_client.session.query(ContextAwarenessRule).count() == 1

    rv = api_client.get(f"/context-awareness-rules/{context_awareness_rule_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_context_awareness_rules(response_content, context_awareness_rule_1.__dict__)


@pytest.mark.parametrize("test_input", [
    (["Rule1", "Sensor1", "NOT_EQUAL", True, True])
])
def test_add_context_awareness_rule(api_client, orm_client, create_sensor,
                                    test_input):
    assert orm_client.session.query(ContextAwarenessRule).count() == 0
    context_awareness_rule_1 = ContextAwarenessRuleDictFactory(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=test_input[2],
        executing=test_input[3],
        value_to_compare_boolean=test_input[4])
    assert orm_client.session.query(ContextAwarenessRule).count() == 0

    rv = api_client.post("/context-awareness-rules/", json=context_awareness_rule_1)
    assert rv.status_code == 200, rv.data
    response_content = json.loads(rv.data)['data']['name']

    # TODO Change to orm_client.session.query...
    rv = api_client.get(f"/context-awareness-rules/{response_content}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_context_awareness_rules(response_content, context_awareness_rule_1)


@pytest.mark.parametrize("test_input, test_modify", [
    (["Rule1", "Sensor1", "NOT_EQUAL", True, True],
     ["Rule1", "Sensor1", "EQUAL", True, True],)
])
def test_update_context_awareness_rule(api_client, orm_client, create_sensor,
                                       test_input, test_modify):
    assert orm_client.session.query(ContextAwarenessRule).count() == 0
    context_awareness_rule_1 = ContextAwarenessRuleFactory2DB(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=ContextAwarenessOperationEnum(test_input[2]),
        executing=test_input[3],
        value_to_compare_boolean=test_input[4])
    assert orm_client.session.query(ContextAwarenessRule).count() == 1

    context_awareness_rule_to_modify = ContextAwarenessRuleDictFactory(
        name=test_modify[0],
        sensor_observed_name=test_modify[1],
        operation_type=test_modify[2],
        executing=test_modify[3],
        value_to_compare_boolean=test_modify[4])

    rv = api_client.put(f"/context-awareness-rules/{context_awareness_rule_1.name}",
                        json=context_awareness_rule_to_modify)
    assert rv.status_code == 200
    assert orm_client.session.query(ContextAwarenessRule).count() == 1

    rv = api_client.get(f"/context-awareness-rules/{context_awareness_rule_1.name}")
    assert rv.status_code == 200
    response_content = json.loads(rv.data)['data']
    assert_context_awareness_rules(response_content, context_awareness_rule_to_modify)


@pytest.mark.parametrize("test_input", [
    (["Rule1", "Sensor1", "NOT_EQUAL", True, True])
])
def test_delete_context_awareness_rule(api_client, orm_client, create_sensor,
                                       test_input):
    assert orm_client.session.query(ContextAwarenessRule).count() == 0
    context_awareness_rule_1 = ContextAwarenessRuleFactory2DB(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=ContextAwarenessOperationEnum(test_input[2]),
        executing=test_input[3],
        value_to_compare_boolean=test_input[4])
    assert orm_client.session.query(ContextAwarenessRule).count() == 1

    rv = api_client.delete(f"/context-awareness-rules/{context_awareness_rule_1.name}")
    assert rv.status_code == 200

    assert orm_client.session.query(ContextAwarenessRule).count() == 0
