import time

import connector_grovepi
from __init__ import ACTUATOR_CONFIGURED
from core import get_actuation, update_actuation
from utils import get_current_time


def trigger_actuation(alarm_trigger, actuation_id, via="NORMAL_LATENCY"):
    if ACTUATOR_CONFIGURED == "BUZZER":
        from main import BUZZER_PIN, GREEN_LED, BLUE_LED

        current_time = get_current_time()

        # Turn all ON
        connector_grovepi.send_digital_value(BUZZER_PIN, alarm_trigger)
        connector_grovepi.send_digital_value(GREEN_LED, alarm_trigger)
        if via == "LOW_LATENCY":
            connector_grovepi.send_digital_value(BLUE_LED, alarm_trigger)

        actuation = get_actuation(actuation_id)
        actuation["time_end"] = current_time
        update_actuation(actuation_id, actuation)

        time.sleep(1)

        # Turn all OFF
        connector_grovepi.send_digital_value(BUZZER_PIN, 0)
        connector_grovepi.send_digital_value(GREEN_LED, 0)
        if via == "LOW_LATENCY":
            connector_grovepi.send_digital_value(BLUE_LED, 0)
