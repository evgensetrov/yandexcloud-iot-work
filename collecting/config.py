import os

ACCESS_KEY = os.getenv("ACCESS_KEY")  # key_id из вывода при создании ключа
SECRET_KEY = os.getenv("SECRET_KEY")  # secret из вывода
BUCKET_NAME = os.getenv("BUCKET_NAME")  # название бакета, к которому имеет доступ сервисный аккаунт, напр. '17062025-iot-data'
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")

schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["timestamp", "deviceId", "data"],
            "properties": {
                "timestamp": {
                "type": "number",
                },
                "deviceId": {
                "type": "string"
                },
                "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["sendorId", "sensorClass", "sensorType", "parameter", "unit", "value"],
                    "properties": {
                    "sendorId": {
                        "type": "string"
                    },
                    "sensorClass": {
                        "type": "string"
                    },
                    "sensorType": {
                        "type": "string"
                    },
                    "parameter": {
                        "type": "string"
                    },
                    "unit": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    }
                    }
                }
                }
            }
        }