from database import session


def add_context_awareness_rule(context_awareness_rule):
    try:
        session.add(context_awareness_rule)
        session.flush()
        name = context_awareness_rule.name
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return name


def get_all_context_awareness_rules():
    from models.ContextAwarenessRule import ContextAwarenessRule

    try:
        context_awareness_rules = session.query(ContextAwarenessRule) \
            .all()
        session.commit()
    except:
        session.rollback()
        return None

    return context_awareness_rules


def get_context_awareness_rule(context_awareness_rule_name):
    from models.ContextAwarenessRule import ContextAwarenessRule

    try:
        context_awareness_rules = session.query(ContextAwarenessRule) \
            .filter_by(name=context_awareness_rule_name) \
            .first()
        session.commit()
    except:
        session.rollback()
        return None

    return context_awareness_rules


def update_context_awareness_rule(context_awareness_rule_name, context_awareness_rule):
    from models.ContextAwarenessRule import ContextAwarenessRule

    try:
        session.query(ContextAwarenessRule) \
            .filter_by(name=context_awareness_rule_name) \
            .update(context_awareness_rule)
        session.commit()
    except Exception as e:
        session.rollback()
        return None

    return context_awareness_rule_name


def delete_context_awareness_rule(context_awareness_rule_name):
    from models.ContextAwarenessRule import ContextAwarenessRule

    try:
        session.query(ContextAwarenessRule) \
            .filter_by(name=context_awareness_rule_name) \
            .delete()
        session.commit()
    except:
        session.rollback()
        return None

    return context_awareness_rule_name
