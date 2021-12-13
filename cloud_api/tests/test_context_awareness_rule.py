import pytest

from fixtures import ContextAwarenessRuleFactory2DB, ThingTypeFactory2DB, ThingFactory2DB, \
    SensorFactory2DB
from models.ContextAwarenessRule import ContextAwarenessOperationEnum


@pytest.fixture
def create_thing_type():
    return ThingTypeFactory2DB(name="Inclinometer")


@pytest.fixture
def create_thing(create_thing_type):
    return ThingFactory2DB(name="ABC-1001", type_name="Inclinometer")


@pytest.fixture
def create_sensor(create_thing):
    return SensorFactory2DB(thing_name="ABC-1001", name="Sensor1")


@pytest.mark.parametrize("test_input, test_output", [
    (["BR1", "Sensor1", "NOT_EQUAL", True, True],
     ["0, BR1, Sensor1, NOT_EQUAL, True, False, True, None, None, None"])
])
def test_context_awareness_rule_to_string(api_client, orm_client, create_sensor,
                                          test_input, test_output):
    context_awareness_rule = ContextAwarenessRuleFactory2DB(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=ContextAwarenessOperationEnum(test_input[2]),
        executing=test_input[3],
        value_to_compare_boolean=test_input[4])

    assert context_awareness_rule.__str__() == test_output[0]


@pytest.mark.parametrize("test_input, test_output", [
    (["BR1", "Sensor1", "NOT_EQUAL", True, True],
     ["0, BR1, Sensor1, NOT_EQUAL, True, True, True, None, None, None"])
])
def test_context_awareness_rule_no_provided_executing_to_string(api_client, orm_client,
                                                                create_sensor,
                                                                test_input, test_output):
    context_awareness_rule = ContextAwarenessRuleFactory2DB(
        name=test_input[0],
        sensor_observed_name=test_input[1],
        operation_type=ContextAwarenessOperationEnum(test_input[2]),
        priority=test_input[3],
        value_to_compare_boolean=test_input[4])

    assert context_awareness_rule.__str__() == test_output[0]
