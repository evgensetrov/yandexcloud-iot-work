CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT PRIMARY KEY,
    description TEXT,
    registry_id TEXT
);

CREATE TABLE IF NOT EXISTS sensors (
    sensor_id TEXT PRIMARY KEY,
    device_id TEXT REFERENCES devices(device_id),
    sensor_class TEXT,
    sensor_type TEXT,
    parameter TEXT,
    unit TEXT
);

CREATE TABLE IF NOT EXISTS averaged_data (
    sensor_id TEXT REFERENCES sensors(sensor_id),
    timestamp TIMESTAMP,
    value DOUBLE PRECISION,
    PRIMARY KEY (sensor_id, timestamp)
);