import time

import connector_grovepi
from __init__ import ACTUATOR_CONFIGURED


def trigger_actuation(alarm_trigger):
    if ACTUATOR_CONFIGURED == "BUZZER":
        from main import BUZZER_PIN, GREEN_LED

        connector_grovepi.send_digital_value(BUZZER_PIN, alarm_trigger)
        connector_grovepi.send_digital_value(GREEN_LED, alarm_trigger)
        time.sleep(1)
        connector_grovepi.send_digital_value(BUZZER_PIN, 0)
        connector_grovepi.send_digital_value(GREEN_LED, 0)
