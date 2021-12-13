from functools import partial

import factory

from models import ContextAwarenessRule
from models.ContextAwarenessRule import ContextAwarenessOperationEnum
from .fixtures import dict_factory


class AbstractContextAwarenessRuleFactory(factory.Factory):
    class Meta:
        model = ContextAwarenessRule
        abstract = True

    id = factory.Sequence(lambda n: int(n))
    name = "Rule1"
    sensor_observed_name = "Sensor1"
    operation_type = ContextAwarenessOperationEnum.equal
    executing = None  # True
    priority = False
    value_to_compare_boolean = None
    value_to_compare_string = None
    value_to_compare_integer = None
    value_to_compare_float = None


class ContextAwarenessRuleFactory(AbstractContextAwarenessRuleFactory):
    pass


ContextAwarenessRuleFactory._meta.exclude = ("id",)
ContextAwarenessRuleDictFactory = partial(dict_factory, ContextAwarenessRuleFactory)


class ContextAwarenessRuleFactory2DB(AbstractContextAwarenessRuleFactory,
                                     factory.alchemy.SQLAlchemyModelFactory):
    """Elements created with this factory are inserted in the DB"""

    class Meta:
        # NOTE Session is assigned on conftest
        sqlalchemy_session_persistence = "commit"
