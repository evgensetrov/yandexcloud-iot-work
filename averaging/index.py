import os
from datetime import datetime
from s3 import list_objects, get_object, delete_object, delete_old_empty_prefixes
from db import initialize_database
from process import process_files
import pytz
from config import TIME_ZONE

def handler(event, context):
    initialize_database()
    print(f'База проинициализирована, собираем данные...')
    all_keys = [key for key in list_objects() if key.endswith('.json')]
    if not all_keys:
        print("Данных не найдено.")
        return
    print(f'Данные собраны, начинаем обработку...')

    processed = process_files(all_keys, get_object)

    now = datetime.now(pytz.timezone(TIME_ZONE))
    print(f'Удаляем данные старше текущего часа из бакета...')

    for key in processed:
        datetime_from_key = key.split('/')[-1].split('.')
        key_datetime = datetime.strptime(datetime_from_key[0], "%Y-%m-%d_%H:%M:%S")

        if now.date() != key_datetime.date() or now.hour > key_datetime.hour:
            delete_object(key)
    print(f'Удаляем пустые директории в бакете...')
    delete_old_empty_prefixes()
    print(f'Готово.')

if __name__ == "__main__":
    handler('', '')