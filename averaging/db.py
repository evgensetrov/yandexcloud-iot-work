import psycopg2
from psycopg2.extras import execute_batch
from config import DB_DSN

def get_connection():
    connection = psycopg2.connect(DB_DSN)
    return connection

def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            with open("schema.sql") as f:
                cur.execute(f.read())
        conn.commit()

def upsert_sensor_data(sensor_entries):
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, """
                INSERT INTO averaged_data (sensor_id, timestamp, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (sensor_id, timestamp)
                DO UPDATE SET value = EXCLUDED.value;
            """, sensor_entries)
        conn.commit()

def upsert_devices_and_sensors(device_id, sensor_meta):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO devices (device_id, description, registry_id)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (device_id, None, None))

            execute_batch(cur, """
                INSERT INTO sensors (sensor_id, device_id, sensor_class, sensor_type, parameter, unit)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, [
                (
                    sensor["sendorId"],
                    device_id,
                    sensor["sensorClass"],
                    sensor["sensorType"],
                    sensor["parameter"],
                    sensor["unit"]
                ) for sensor in sensor_meta
            ])
        conn.commit()