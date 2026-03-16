import json
from typing import Any
import paho.mqtt.client as mqtt
from gpiozero import LED
import pymysql
from datetime import datetime, timezone
from typing import Any, Optional

#===================================
# Paramètres MQTT
#===================================
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

#===================================
# Paramètres MariaDB
#===================================
DB_HOST = "localhost"
DB_USER = "iot"
DB_PASSWORD = "iot"
DB_NAME = "iot_b3"

def utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

def db_connect() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True,
        charset="utf8mb4",
    )

db = db_connect()

#===================================
# Fonctions utilitaires LED
#===================================
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
        

#===================================
# Fonctions utilitaires DB
#===================================
def extract_device(topic: str) -> str:
    parts = topic.split("/")
    return parts[4] if len(parts) >= 5 else "unknown"

def is_telemetry(topic: str) -> bool:
    if "/sensors/" not in topic:
        return False
    if topic.endswith("/value"):
        return False
    return True

def classify_kind(topic: str) -> str:
    if "/cmd/" in topic:
        return "cmd"
    if "/state/" in topic:
        return "state"
    if "/status/" in topic:
        return "status"
    return "other"

def try_parse_json(payload_text: str) -> Optional[dict[str, Any]]:
    try:
        obj = json.loads(payload_text)
        return obj if isinstance(obj, dict) else None
    except json.JSONDecodeError:
        return None

#===================================
# Insertion dans la DB
#===================================
def insert_telemetry(ts_utc: datetime, device: str, topic:str, payload_text:str) -> None:
    obj = try_parse_json(payload_text)
    value = None
    unit = None

    if obj is not None:
        if "value" in obj:
            try:
                value = float(obj["value"])
            except (TypeError, ValueError):
                value = None
        if "unit" in obj and isinstance(obj["unit"], str):
            unit = obj["unit"][:16]
    
    sql = """
        INSERT INTO telemetry (ts_utc, device, topic, value, unit, payload)
        VALUES (%s, %s, %s, %s, %s, %s)        
        """

    with db.cursor() as cur:
        cur.execute(sql, (ts_utc, device, topic, value, unit, payload_text))


def insert_event(ts_utc:datetime, device:str, topic: str, kind:str, payload_text: str) -> None:
    sql = """
        INSERT INTO events (ts_utc, device, topic, kind, payload)
        VALUES (%s, %s, %s, %s, %s)
        """
    with db.cursor() as cur:
        cur.execute(sql, (ts_utc, device, topic, kind, payload_text))
        
#===================================
# Callback MQTT
#===================================
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"[CONNECT] reason_code={reason_code}")
    if reason_code == 0:

        client.subscribe(TOPIC_CMD, qos=QOS_CMD)
        print(f"[SUB] {TOPIC_CMD} (qos={QOS_CMD})")

        
        publish_led_state(client)
        
def on_message(client, userdata, msg: mqtt.MQTTMessage):
    payload_text = msg.payload.decode("utf-8", errors="replace")
    print(f"[MSG] topic={msg.topic} qos={msg.qos} retain={msg.retain} payload={payload_text}")
    command = parse_command(payload_text)
    if command is None:
        print("[WARN] Commande invalide (JSON attendu). Ignorée.")
        return
    
    # Action GPIO
    if command == "on":
        led.on()
    else:
        led.off()

    
    publish_led_state(client)
def on_disconnect(client, userdata, reason_code, properties=None):
    print(f"[DISCONNECT] reason_code={reason_code}")
    led.off()

#===================================
# Démarrage du client MQTT
#===================================
client = mqtt.Client(client_id=CLIENT_ID, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.reconnect_delay_set(min_delay=1, max_delay=30)

client.connect(BROKER_HOST, BROKER_PORT, keepalive=KEEPALIVE_S)
client.loop_forever()