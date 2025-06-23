import sender
import emulator
import time
import json
import os

# DEVICE_ID="areal1og31pb568e2vfo"
# DEVICE_CLASS="EnvironmentalSensor"
# DEVICE_TYPE="Temperature"

DEVICE_ID = os.getenv("DEVICE_ID")
DEVICE_CLASS = os.getenv("DEVICE_CLASS")
DEVICE_TYPE = os.getenv("DEVICE_TYPE")

TIME_TO_EMULATE = os.getenv("TIME_TO_EMULATE")  # "NOW" или timestamp
SENSOR_AMOUNT = int(os.getenv("SENSOR_AMOUNT"))  # количество сенсоров для эмуляции

MQTT_BROKER = "mqtt.cloud.yandex.net"
MQTT_PORT = 8883
MQTT_TOPIC = f"$devices/{DEVICE_ID}/events"

CA_CERT = "rootCA.crt"  # Путь до сертификатов - по умолчанию, лежат в директории проекта
CLIENT_CERT = "cert.pem"
CLIENT_KEY = "key.pm"

sensor_map = {
    "EnvironmentalSensor": {
        "Temperature": emulator.Sensor.EnvironmentalSensor.Temperature(sensor_amount=SENSOR_AMOUNT),
        "Humidity": emulator.Sensor.EnvironmentalSensor.Humidity(sensor_amount=SENSOR_AMOUNT),
        "AirQuality": emulator.Sensor.EnvironmentalSensor.AirQuality(sensor_amount=SENSOR_AMOUNT),
        "CO2": emulator.Sensor.EnvironmentalSensor.CO2(sensor_amount=SENSOR_AMOUNT),
        "Light": emulator.Sensor.EnvironmentalSensor.Light(sensor_amount=SENSOR_AMOUNT),
        "Noise": emulator.Sensor.EnvironmentalSensor.Noise(sensor_amount=SENSOR_AMOUNT),
        "WindSpeed": emulator.Sensor.EnvironmentalSensor.WindSpeed(sensor_amount=SENSOR_AMOUNT),
        "WindDirection": emulator.Sensor.EnvironmentalSensor.WindDirection(sensor_amount=SENSOR_AMOUNT),
        "Rainfall": emulator.Sensor.EnvironmentalSensor.Rainfall(sensor_amount=SENSOR_AMOUNT),
        "Pressure": emulator.Sensor.EnvironmentalSensor.Pressure(sensor_amount=SENSOR_AMOUNT)
    },
    "LocationSensor": {
        "GPS": emulator.Sensor.LocationSensor.GPS(sensor_amount=SENSOR_AMOUNT),
    },
    "PowerSensor": {
        "Voltage": emulator.Sensor.PowerSensor.Voltage(sensor_amount=SENSOR_AMOUNT),
        "Current": emulator.Sensor.PowerSensor.Current(sensor_amount=SENSOR_AMOUNT),
        "PowerConsumption": emulator.Sensor.PowerSensor.PowerConsumption(sensor_amount=SENSOR_AMOUNT)
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

sensor = sensor_map[DEVICE_CLASS][DEVICE_TYPE]

def handler(event, context):
    if TIME_TO_EMULATE == "NOW":
        values = sensor.get_values()

        data = json_data = {
            "timestamp": time.time(),
            "sensorId": DEVICE_ID,
            "sensorClass": DEVICE_CLASS,
            "sensorType": DEVICE_TYPE,
            "data": [
                {
                    "parameter": parameter_map[DEVICE_CLASS][DEVICE_TYPE],
                    "unit": unit_map[DEVICE_CLASS][DEVICE_TYPE],
                    "value": values[i]
                } for i in range(len(values))
            ]
        }
        
    else:
        from datetime import datetime
        import pytz
        timezone = pytz.timezone("Europe/Moscow")

        try:
            timestamp = float(TIME_TO_EMULATE)
            time_ = datetime.fromtimestamp(timestamp, timezone)
            values = sensor.get_values(time_)
        except Exception as e:
            print(f"Произошла ошибка. Проверьте, что переменная TIME_TO_EMULATE имеет тип float или значение 'NOW'.\nОшибка: {str(e)}")

        data = json_data = {
            "timestamp": timestamp,
            "sensorId": DEVICE_ID,
            "sensorClass": DEVICE_CLASS,
            "sensorType": DEVICE_TYPE,
            "data": [
                {
                    "parameter": parameter_map[DEVICE_CLASS][DEVICE_TYPE],
                    "unit": unit_map[DEVICE_CLASS][DEVICE_TYPE],
                    "value": values[i]
                } for i in range(len(values))
            ]
        }

    send_result = sender.main(CA_CERT, CLIENT_CERT, CLIENT_KEY, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, json.dumps(data))
    print(send_result)

