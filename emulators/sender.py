import ssl
import random
import os
from paho.mqtt import client as mqtt

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_TYPE = os.getenv("DEVICE_TYPE")  # тип датчика из types.yaml

MQTT_BROKER = "mqtt.cloud.yandex.net"
MQTT_PORT = 8883
MQTT_TOPIC = f"$devices/{DEVICE_ID}/events"

CA_CERT = "rootCA.crt"
CLIENT_CERT = "cert.pem"
CLIENT_KEY = "key.pm"


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.connect(MQTT_BROKER, MQTT_PORT)
temperature = round(random.uniform(20.0, 30.0), 2)
payload = f'{{"temperature": {temperature}}}'
result = client.publish(MQTT_TOPIC, payload)
status = result[0]
if status == 0:
    print(f"Успешно отправлено в топик {MQTT_TOPIC}. \nСообщение:\n{payload}")
else:
    print(f"Не удалось отправить сообщение. \nСообщение:\n{payload}")
