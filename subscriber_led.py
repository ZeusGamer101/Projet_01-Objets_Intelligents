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




