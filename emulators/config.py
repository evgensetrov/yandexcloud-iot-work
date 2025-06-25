import os
import ast

DEVICE_ID = os.getenv("DEVICE_ID")

SENSORS_CLASSES = ast.literal_eval(os.getenv("SENSORS_CLASSES"))
SENSORS_TYPES = ast.literal_eval(os.getenv("SENSORS_TYPES"))
SENSORS_IDS = ast.literal_eval(os.getenv("SENSORS_IDS"))

TIME_TO_EMULATE = os.getenv("TIME_TO_EMULATE")  # "NOW" или timestamp

MQTT_BROKER = "mqtt.cloud.yandex.net"
MQTT_PORT = 8883
MQTT_TOPIC = f"$devices/{DEVICE_ID}/events"

CA_CERT = "rootCA.crt"  # Путь до сертификатов - по умолчанию, лежат в директории проекта
CLIENT_CERT = "cert.pem"
CLIENT_KEY = "key.pm"