from flask_restful import reqparse

from app import logger
from errors.api_errors import GENERIC, NOT_EXISTS_ID, FIELD_NOT_VALID, EXISTS_ID
from models import ContextAwarenessRule
from models.ContextAwarenessRule import ContextAwarenessOperationEnum
from resources import Resource, Response
from translators import api_translators as translator
from validators.api_validators import ContextAwarenessRuleValidator

context_awareness_rule_parser = reqparse.RequestParser()
context_awareness_rule_parser.add_argument("name", type=str)
context_awareness_rule_parser.add_argument("sensor_observed_name", type=str)
context_awareness_rule_parser.add_argument("operation_type", type=str)
context_awareness_rule_parser.add_argument("executing", type=bool, required=False)
context_awareness_rule_parser.add_argument("priority", type=bool, required=False)
context_awareness_rule_parser.add_argument("value_to_compare_boolean", type=bool, required=False)
context_awareness_rule_parser.add_argument("value_to_compare_string", type=str, required=False)
context_awareness_rule_parser.add_argument("value_to_compare_integer", type=int, required=False)
context_awareness_rule_parser.add_argument("value_to_compare_float", type=float, required=False)


class ContextAwarenessRulesHandler:
    class ContextAwarenessRules(Resource):
        def get(self):
            logger.debug("[GET] /context-awareness-rules/")
            response = self.repository.context_awareness_rule_repository. \
                get_all_context_awareness_rules()

            return Response.success(
                [translator.context_awareness_rule_translator(context_awareness_rule)
                 for context_awareness_rule in response])

        def post(self):
            logger.debug("[POST] /context-awareness-rules/")
            args = context_awareness_rule_parser.parse_args()

            # Get ContextAwarenessRule arguments
            if ContextAwarenessRuleValidator.is_name_valid(args["name"]):
                name = args["name"]

                response = self.repository.context_awareness_rule_repository. \
                    get_context_awareness_rule(name)
                if response:
                    return Response.error(EXISTS_ID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ContextAwarenessRuleValidator.is_sensor_observed_valid(args["sensor_observed_name"]):
                sensor_observed_name = args["sensor_observed_name"]

                response = self.repository.sensor_repository.get_sensor(sensor_observed_name)

                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ContextAwarenessRuleValidator.is_operation_type_valid(args["operation_type"]):
                operation_type = args["operation_type"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ContextAwarenessRuleValidator.is_executing_valid(args["executing"]):
                executing = args["executing"]
            else:
                executing = True

            if ContextAwarenessRuleValidator.is_priority_valid(args["priority"]):
                priority = args["priority"]
            else:
                priority = False

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_boolean_valid(args["value_to_compare_boolean"]):
                value_to_compare_boolean = args["value_to_compare_boolean"]
            else:
                value_to_compare_boolean = None

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_string_valid(args["value_to_compare_string"]):
                value_to_compare_string = args["value_to_compare_string"]
            else:
                value_to_compare_string = None

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_integer_valid(args["value_to_compare_integer"]):
                value_to_compare_integer = args["value_to_compare_integer"]
            else:
                value_to_compare_integer = None

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_float_valid(args["value_to_compare_float"]):
                value_to_compare_float = args["value_to_compare_float"]
            else:
                value_to_compare_float = None

            context_awareness_rule = ContextAwarenessRule(
                name=name,
                sensor_observed_name=sensor_observed_name,
                operation_type=ContextAwarenessOperationEnum(operation_type),
                executing=executing,
                priority=priority,
                value_to_compare_boolean=value_to_compare_boolean,
                value_to_compare_string=value_to_compare_string,
                value_to_compare_integer=value_to_compare_integer,
                value_to_compare_float=value_to_compare_float
            )

            result = self.repository.context_awareness_rule_repository. \
                add_context_awareness_rule(context_awareness_rule)
            if result:
                return Response.success({"name": result})

            return Response.error(GENERIC)

    class ContextAwarenessRule(Resource):
        def get(self, context_awareness_rule_name):
            logger.debug(f"[GET] /context-awareness-rules/{context_awareness_rule_name}")
            response = self.repository.context_awareness_rule_repository. \
                get_context_awareness_rule(context_awareness_rule_name)

            if response:
                return Response.success(translator.context_awareness_rule_translator(response))
            return Response.error(NOT_EXISTS_ID)

        def put(self, context_awareness_rule_name):
            logger.debug(f"[PUT] /context-awareness-rules/{context_awareness_rule_name}")
            args = context_awareness_rule_parser.parse_args()

            response = self.repository.context_awareness_rule_repository. \
                get_context_awareness_rule(context_awareness_rule_name)
            if response is None:
                return Response.error(NOT_EXISTS_ID)

            # Get ContextAwarenessRule arguments
            if ContextAwarenessRuleValidator.is_sensor_observed_valid(args["sensor_observed_name"]):
                sensor_observed_name = args["sensor_observed_name"]

                response = self.repository.sensor_repository.get_sensor(sensor_observed_name)

                if response is None:
                    return Response.error(FIELD_NOT_VALID)
            else:
                return Response.error(FIELD_NOT_VALID)

            if ContextAwarenessRuleValidator.is_operation_type_valid(args["operation_type"]):
                operation_type = args["operation_type"]
            else:
                return Response.error(FIELD_NOT_VALID)

            if ContextAwarenessRuleValidator.is_executing_valid(args["executing"]):
                executing = args["executing"]
            else:
                executing = True

            if ContextAwarenessRuleValidator.is_priority_valid(args["priority"]):
                priority = args["priority"]
            else:
                priority = False

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_boolean_valid(args["value_to_compare_boolean"]):
                value_to_compare_boolean = args["value_to_compare_boolean"]
            else:
                value_to_compare_boolean = None

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_string_valid(args["value_to_compare_string"]):
                value_to_compare_string = args["value_to_compare_string"]
            else:
                value_to_compare_string = None

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_integer_valid(args["value_to_compare_integer"]):
                value_to_compare_integer = args["value_to_compare_integer"]
            else:
                value_to_compare_integer = None

            if ContextAwarenessRuleValidator. \
                    is_value_to_compare_float_valid(args["value_to_compare_float"]):
                value_to_compare_float = args["value_to_compare_float"]
            else:
                value_to_compare_float = None

            context_awareness_rule = {
                "name": context_awareness_rule_name,
                "sensor_observed_name": sensor_observed_name,
                "operation_type": ContextAwarenessOperationEnum(operation_type),
                "executing": executing,
                "priority": priority,
                "value_to_compare_boolean": value_to_compare_boolean,
                "value_to_compare_string": value_to_compare_string,
                "value_to_compare_integer": value_to_compare_integer,
                "value_to_compare_float": value_to_compare_float
            }

            response = self.repository.context_awareness_rule_repository. \
                update_context_awareness_rule(context_awareness_rule_name, context_awareness_rule)
            if response:
                return Response.success({"name": response})

            return Response.error(GENERIC)

        def delete(self, context_awareness_rule_name):
            logger.debug(f"[DELETE] /context-awareness-rules/{context_awareness_rule_name}")
            response = self.repository.context_awareness_rule_repository.get_context_awareness_rule(
                context_awareness_rule_name)

            if response is None:
                return Response.error(NOT_EXISTS_ID)

            result = self.repository.context_awareness_rule_repository.delete_context_awareness_rule(
                context_awareness_rule_name)
            if result:
                return Response.success({"name": result})
            return Response.error(GENERIC)
