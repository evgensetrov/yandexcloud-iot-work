import os

DB_DSN      = os.getenv("DB_DSN", "postgresql://user:postgres@rc1d-4l7rl7uudkcqpecj.mdb.yandexcloud.net:6432/iot")
BUCKET_NAME = os.getenv("BUCKET_NAME", "iot-bucket-spring2025")
ACCESS_KEY  = os.getenv("ACCESS_KEY", "YCAJErfB5TTbdi5pdSq4_ri35")  # key_id из вывода при создании ключа
SECRET_KEY  = os.getenv("SECRET_KEY", "YCNZtkCndsUsUEsaVY7PqmhoDXxuKz4xGIHQzk4G")  # secret из вывода
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")