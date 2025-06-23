import os
import datetime
import pytz
import boto3
import base64
import logging
import json

ACCESS_KEY = os.getenv("ACCESS_KEY")  # key_id из вывода при создании ключа
SECRET_KEY = os.getenv("SECRET_KEY")  # secret из вывода
BUCKET_NAME = os.getenv("BUCKET_NAME")  # название бакета, к которому имеет доступ сервисный аккаунт, напр. '17062025-iot-data'
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")

session = boto3.session.Session()
s3 = session.client(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )

def handler(event, context):
    print(f'Начало обработки функции')
    print(f'event: {event}')
    try:
        message = event.get("messages", [])[0]
        details = message.get("details")

        registry_id = details["registry_id"]
        device_id = details["device_id"]
        payload_str = base64.b64decode(details["payload"]).decode('utf-8')
        payload = json.loads(payload_str)
        timestamp = payload["timestamp"]

        # now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
        now = datetime.datetime.fromtimestamp(timestamp, tz=pytz.timezone(TIME_ZONE))
        
        timestamp_str = now.strftime("%Y-%m-%d_%H:%M:%S.%f")[:-3]

        print(f'Форматированный timestamp: {timestamp_str}')

        key = f"{registry_id}/{device_id}/{now:%Y-%m/%d}/{timestamp_str}.json"
        print(f'Путь до объекта: {key}')

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=payload_str.encode('utf-8'),
            ContentType='application/json'
        )
        print(f"Событие успешно обработано, сообщение положено в {key}")

        return {
            "statusCode": 200,
            "body": f"Событие успешно обработано, сообщение положено в {key}"
        }

    except Exception as e:
        print(f'Произошла ошибка: {str(e)}')
        return {
            "statusCode": 500,
            "body": f"Ошибка: {str(e)}\n\nTrigger event: {event}"
        }