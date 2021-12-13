# -*- coding: utf-8 -*-
import enum

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum

from database import Base


class ContextAwarenessOperationEnum(enum.Enum):
    not_equal = "NOT_EQUAL"
    equal = "EQUAL"
    less_than = "LESS_THAN"
    more_than = "MORE_THAN"


class ContextAwarenessRule(Base):
    __tablename__ = "context_awareness_rule"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(32), unique=True, nullable=False)
    sensor_observed_name = Column(String(32), ForeignKey("sensor.name", ondelete="SET NULL"))
    operation_type = Column(Enum(ContextAwarenessOperationEnum), nullable=False)
    executing = Column(Boolean, default=True)
    priority = Column(Boolean, default=False)
    value_to_compare_boolean = Column(Boolean)
    value_to_compare_string = Column(String(32))
    value_to_compare_integer = Column(Integer)
    value_to_compare_float = Column(Float)

    def __str__(self):
        return f"{self.id}, {self.name}, {self.sensor_observed_name}, " \
               f"{self.operation_type.value}, {self.executing}, {self.priority}, " \
               f"{self.value_to_compare_boolean}, {self.value_to_compare_string}, " \
               f"{self.value_to_compare_integer}, {self.value_to_compare_float}"
