import ssl
from paho.mqtt import client as mqtt

def connect_mqtt(CA_CERT, CLIENT_CERT, CLIENT_KEY, MQTT_BROKER, MQTT_PORT):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()

    return client

def send_data(client, MQTT_TOPIC, data):
    result = client.publish(MQTT_TOPIC, data)
    result.wait_for_publish() 
    return result

def main(CA_CERT, CLIENT_CERT, CLIENT_KEY, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, data):
    client = connect_mqtt(CA_CERT, CLIENT_CERT, CLIENT_KEY, MQTT_BROKER, MQTT_PORT)
    result = send_data(client, MQTT_TOPIC, data)
    client.loop_stop()
    client.disconnect()
    status = result[0]
    if status == 0:
        return f"Успешно отправлено в топик {MQTT_TOPIC}. \nСообщение:\n{data}"
    else:
        return f"Не удалось отправить сообщение. \nСообщение:\n{data}"
