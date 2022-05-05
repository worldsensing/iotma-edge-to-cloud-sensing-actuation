from datetime import datetime


def get_value_to_compare_from_context_awareness_rule(context_awareness_rule):
    if context_awareness_rule["value_to_compare_boolean"] is not None:
        return context_awareness_rule["value_to_compare_boolean"]
    elif context_awareness_rule["value_to_compare_string"] is not None:
        return context_awareness_rule["value_to_compare_string"]
    elif context_awareness_rule["value_to_compare_integer"] is not None:
        return context_awareness_rule["value_to_compare_integer"]
    elif context_awareness_rule["value_to_compare_float"] is not None:
        return context_awareness_rule["value_to_compare_float"]

    return None


def get_current_time():
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S.%f%z")
