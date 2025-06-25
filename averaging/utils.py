from datetime import datetime, timedelta

def round_to_next_5min(dt):
    minute = (dt.minute // 5 + 1) * 5
    return dt.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minute)

def parse_json_file(content):
    import json
    return json.loads(content)

def extract_sensor_entries(json_data):
    ts = datetime.fromtimestamp(json_data["timestamp"])
    entries = []
    device_id = json_data["deviceId"]
    for sensor in json_data["data"]:
        entries.append({
            "timestamp": ts,
            "sensor_id": sensor["sendorId"],
            "value": sensor["value"]
        })
    return entries