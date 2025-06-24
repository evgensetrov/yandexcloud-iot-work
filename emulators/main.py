import sender
import emulator
import time
import json
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

sensor_map = {
    "EnvironmentalSensor": {
        "Temperature": emulator.Sensor.EnvironmentalSensor.Temperature(),
        "Humidity": emulator.Sensor.EnvironmentalSensor.Humidity(),
        "AirQuality": emulator.Sensor.EnvironmentalSensor.AirQuality(),
        "CO2": emulator.Sensor.EnvironmentalSensor.CO2(),
        "Light": emulator.Sensor.EnvironmentalSensor.Light(),
        "Noise": emulator.Sensor.EnvironmentalSensor.Noise(),
        "WindSpeed": emulator.Sensor.EnvironmentalSensor.WindSpeed(),
        "WindDirection": emulator.Sensor.EnvironmentalSensor.WindDirection(),
        "Rainfall": emulator.Sensor.EnvironmentalSensor.Rainfall(),
        "Pressure": emulator.Sensor.EnvironmentalSensor.Pressure()
    },
    "LocationSensor": {
        "GPS": emulator.Sensor.LocationSensor.GPS(),
    },
    "PowerSensor": {
        "Voltage": emulator.Sensor.PowerSensor.Voltage(),
        "Current": emulator.Sensor.PowerSensor.Current(),
        "PowerConsumption": emulator.Sensor.PowerSensor.PowerConsumption()
    }
}

parameter_map = {
    "EnvironmentalSensor": {
        "Temperature": "Температура окружающей среды",
        "Humidity": "Относительная влажность",
        "AirQuality": "Индекс качества воздуха",
        "CO2": "Концентрация CO₂",
        "Light": "Освещённость",
        "Noise": "Уровень шума",
        "WindSpeed": "Скорость ветра",
        "WindDirection": "Направление ветра",
        "Rainfall": "Осадки",
        "Pressure": "Атмосферное давление"
    },
    "LocationSensor": {
        "GPS": "Координаты GPS"
    },
    "PowerSensor": {
        "Voltage": "Напряжение",
        "Current": "Сила тока",
        "PowerConsumption": "Потребляемая мощность"
    }
}

unit_map = {
    "EnvironmentalSensor": {
        "Temperature": "°C",
        "Humidity": "%",
        "AirQuality": "AQI",
        "CO2": "ppm",
        "Light": "лк", 
        "Noise": "дБ",
        "WindSpeed": "м/с",
        "WindDirection": "°",
        "Rainfall": "мм",
        "Pressure": "гПа"
    },
    "LocationSensor": {
        "GPS": "°"
    },
    "PowerSensor": {
        "Voltage": "В",
        "Current": "А",
        "PowerConsumption": "Вт"
    }
}

sensors = [sensor_map[SENSORS_CLASSES[i]][SENSORS_TYPES[i]] for i in range(len(SENSORS_CLASSES))]

def handler(event, context):
    if TIME_TO_EMULATE == "NOW":

        data = {
            "timestamp": time.time(),
            "deviceId": DEVICE_ID,
            "data": [
                {
                    "sendorId": SENSORS_IDS[i],
                    "sensorClass": SENSORS_CLASSES[i],
                    "sensorType": SENSORS_TYPES[i],
                    "parameter": parameter_map[SENSORS_CLASSES[i]][SENSORS_TYPES[i]],
                    "unit": unit_map[SENSORS_CLASSES[i]][SENSORS_TYPES[i]],
                    "value": sensors[i].get_value()
                } for i in range(len(SENSORS_CLASSES))
            ]
        }
        
    else:
        from datetime import datetime
        import pytz
        timezone = pytz.timezone("Europe/Moscow")

        try:
            timestamp = float(TIME_TO_EMULATE)
            time_ = datetime.fromtimestamp(timestamp, timezone)
        except Exception as e:
            print(f"Произошла ошибка. Проверьте, что переменная TIME_TO_EMULATE имеет тип float или значение 'NOW'.\nОшибка: {str(e)}")

        data = {
            "timestamp": time.time(),
            "deviceId": DEVICE_ID,
            "data": [
                {
                    "sendorId": SENSORS_IDS[i],
                    "sensorClass": SENSORS_CLASSES[i],
                    "sensorType": SENSORS_TYPES[i],
                    "parameter": parameter_map[SENSORS_CLASSES[i]][SENSORS_TYPES[i]],
                    "unit": unit_map[SENSORS_CLASSES[i]][SENSORS_TYPES[i]],
                    "value": sensors[i].get_value(time_)
                } for i in range(len(SENSORS_CLASSES))
            ]
        }

    send_result = sender.main(CA_CERT, CLIENT_CERT, CLIENT_KEY, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, json.dumps(data))
    print(send_result)

