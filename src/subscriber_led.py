import json
from typing import Any
import paho.mqtt.client as mqtt
from gpiozero import LED

# Paramètres
BROKER_HOST = "localhost"
BROKER_PORT = 1883
KEEPALIVE_S = 60

TEAM = "equipe_blondel_martin"
DEVICE = "piBM"

CLIENT_ID = "b3-sub-piBM-led"

LED_PIN_BCM = 17
led = LED(LED_PIN_BCM)

TOPIC_CMD = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/led/cmd"
TOPIC_STATE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/actuators/led/cmd"

QOS_CMD = 1

def publish_led_state(client: mqtt.Client) -> None:
    state = "on" if led.is_lit else "off"
    client.publish(TOPIC_STATE, state, qos=1, retain=True)
    print(f"[STATE] {TOPIC_STATE} -> {state}")


def parse_command(payload_text: str) -> str | None:
    try:
        data: dict[str, Any] = json.loads(payload_text)
    except json.JSONDecodeError:
        return None
    
    # Normalisation des données
    if "state" in data and isinstance(data["state"], str):
        s = data["state"].strip().lower()
        if s in ("on", "off"):
            return s
    
    if "value" in data:
        v = data["value"]
        if v in (1, True, "1", "on", "ON"):
            return "on"
        if v in (0, False, "0", "off", "OFF"):
            return "off"