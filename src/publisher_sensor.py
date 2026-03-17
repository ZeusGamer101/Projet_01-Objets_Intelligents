from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

#---------------------------------------------------------------------
# 1) Param�tres MQTT 
# ---------------------------------------------------------------------

BROKER_HOST = "localhost" 
BROKER_PORT = 1883 
KEEPALIVE_S = 60 

TEAM = "equipe_blondel_martin"
DEVICE = "piBM"

CLIENT_ID = "b3-sub-piBM-led"

TOPIC_JSON = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/sensors/temperature"
TOPIC_VALUE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/sensors/temperature/value"

# Statut "online/offline" pratique en IoT (peut �tre affich� aussi dans un dashboard)
TOPIC_ONLINE = f"ahuntsic/aec-iot/b3/{TEAM}/{DEVICE}/status/online"

# QoS:
# - capteurs fr�quents -> QoS 0 (rapide, pas d'ack)
# - �tats/commandes -> souvent QoS 1 (plus fiable)

QOS_SENSOR = 0
QOS_STATUS = 1
PUBLISH_PERIOD_S = 2.0

# ---------------------------------------------------------------------
# 2) Lecture capteur (� brancher sur VOTRE code du cours pr�c�dent)
# ---------------------------------------------------------------------

def read_temperature_c() -> float:
    return round(20.0 + random.random() * 5.0, 2)


# ---------------------------------------------------------------------
# 3) Callbacks MQTT (�v�nementiel)
# ---------------------------------------------------------------------

connected = False # drapeau simple pour savoir si on est connect�

def on_connect(client, userdata, flags, reason_code, properties=None):
    global connected
    print("[CONNECT] reason_code={reason_code}")
    connected = (reason_code == 0)


def on_disconnect(client,userdata,reason_code,properties=None):
    global connected
    print(f"[DISCONNECT] reason_code={reason_code}")
    connected = False