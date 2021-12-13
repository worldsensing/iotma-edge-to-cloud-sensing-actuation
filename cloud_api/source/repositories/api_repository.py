# -*- coding: utf-8 -*-
from repositories.actuatable_property_repository import ActuatablePropertyRepository
from repositories.actuation_repository import ActuationRepository
from repositories.actuator_repository import ActuatorRepository
from repositories.context_awareness_rule_repository import ContextAwarenessRuleRepository
from repositories.feature_of_interest_repository import FeatureOfInterestRepository
from repositories.location_repository import LocationRepository
from repositories.observable_property_repository import ObservablePropertyRepository
from repositories.observation_repository import ObservationRepository
from repositories.platform_repository import PlatformRepository
from repositories.sensor_repository import SensorRepository
from repositories.thing_repository import ThingRepository
from repositories.thing_type_repository import ThingTypeRepository


class ApiRepository:
    actuatable_property_repository = ActuatablePropertyRepository
    actuation_repository = ActuationRepository
    actuator_repository = ActuatorRepository
    context_awareness_rule_repository = ContextAwarenessRuleRepository
    feature_of_interest_repository = FeatureOfInterestRepository
    location_repository = LocationRepository
    observable_property_repository = ObservablePropertyRepository
    observation_repository = ObservationRepository
    platform_repository = PlatformRepository
    sensor_repository = SensorRepository
    thing_repository = ThingRepository
    thing_type_repository = ThingTypeRepository
