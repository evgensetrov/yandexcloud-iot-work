import os
import datetime
import pytz
import boto3
import base64
import logging
import json
from jsonschema import validate, ValidationError
from config import ACCESS_KEY, SECRET_KEY, TIME_ZONE, BUCKET_NAME, schema

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

        validate(instance=payload, schema=schema)

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
    
    except ValidationError as ve:
        print(f'Произошла ошибка валидации данных: {str(ve)}\nДанные, не прошедшие валидацию:\n{payload_str}') # type: ignore

    except Exception as e:
        print(f'Произошла ошибка: {str(e)}')
        return {
            "statusCode": 500,
            "body": f"Ошибка: {str(e)}\n\nTrigger event: {event}"
        }