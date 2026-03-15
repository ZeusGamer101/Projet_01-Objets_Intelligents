import json
from typing import Any
import paho.mqtt.client as mqtt
from gpiozero import LED

#===================================
# Paramètres
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
# Fonctions utilitaires
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