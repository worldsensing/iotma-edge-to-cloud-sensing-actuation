from database import context_awareness_rule


class ContextAwarenessRuleRepository:
    @staticmethod
    def add_context_awareness_rule(context_awareness_rule_obj):
        return context_awareness_rule.add_context_awareness_rule(context_awareness_rule_obj)

    @staticmethod
    def get_all_context_awareness_rules():
        return context_awareness_rule.get_all_context_awareness_rules()

    @staticmethod
    def get_context_awareness_rule(context_awareness_rule_name):
        return context_awareness_rule.get_context_awareness_rule(context_awareness_rule_name)

    @staticmethod
    def update_context_awareness_rule(context_awareness_rule_name, context_awareness_rule_obj):
        return context_awareness_rule.update_context_awareness_rule(context_awareness_rule_name,
                                                                    context_awareness_rule_obj)

    @staticmethod
    def delete_context_awareness_rule(context_awareness_rule_name):
        return context_awareness_rule.delete_context_awareness_rule(context_awareness_rule_name)
