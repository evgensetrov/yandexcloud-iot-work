from collections import defaultdict
from datetime import timedelta
from utils import parse_json_file, extract_sensor_entries
from db import upsert_sensor_data, upsert_devices_and_sensors

def aggregate_entries_by_5min(entries):
    groups = {}

    for entry in entries:
        sensor_id = entry["sensor_id"]
        ts = entry["timestamp"].replace(second=0, microsecond=0)

        rounded_minute = ((ts.minute // 5) + 1) * 5
        interval_time = ts.replace(minute=0) + timedelta(minutes=rounded_minute)

        key = (sensor_id, interval_time)
        if key not in groups:
            groups[key] = []
        groups[key].append(entry["value"])

    result = []
    for (sensor_id, timestamp), values in groups.items():
        average = sum(values) / len(values)
        result.append((sensor_id, timestamp, average))

    return result

def process_files(keys, s3_get_func):
    all_entries = []
    all_devices = []
    for i, key in enumerate(keys):
        if i%100 == 0:
            print(f'Обработано {i} объектов из {len(keys)}')
        try:
            raw = s3_get_func(key)
            data = parse_json_file(raw)
            if data["deviceId"] not in all_devices:
                upsert_devices_and_sensors(data["deviceId"], data["data"])
                all_devices.append(data["deviceId"])
            entries = extract_sensor_entries(data)
            all_entries.extend(entries)
        except Exception as e:
            print(f"Error processing {key}: {e}")
    print(f'Данные обработаны, начинаем усреднение...')
    aggregated = aggregate_entries_by_5min(all_entries)
    print(f'Данные усреднены, записываем в базу...')
    upsert_sensor_data(aggregated)
    print(f'Данные записаны в базу')
    return keys