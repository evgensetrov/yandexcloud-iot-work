import boto3
import json
from datetime import datetime
from config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME

session = boto3.session.Session()
s3 = session.client(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )


def list_objects(prefix=""):
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        for obj in page.get("Contents", []):
            yield obj['Key']

def get_object(key):
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    return obj['Body'].read()

def delete_object(key):
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)

def delete_old_empty_prefixes():
    all_keys = list(list_objects())
    today = datetime.now().strftime("%Y-%m-%d")
    folders = set(key.split("/")[0] for key in all_keys if "/" in key)

    for folder in folders:
        if folder != today:
            if not any(key.startswith(folder + "/") and key.endswith(".json") for key in all_keys):
                print(f"Deleting empty folder: {folder}")
                delete_objects_with_prefix(folder + "/")

def delete_objects_with_prefix(prefix):
    keys = list(list_objects(prefix))
    if keys:
        s3.delete_objects(Bucket=BUCKET_NAME, Delete={
            'Objects': [{'Key': key} for key in keys]
        })