#!/bin/bash

export TF_VAR_token=$(yc iam create-token | tr -d '\r\n')
export TF_VAR_folder_id=$(yc config get folder-id | tr -d '\r\n')
export TF_VAR_cloud_id=$(yc config get cloud-id | tr -d '\r\n')

echo "--- Ресурсы будут созданы в folder_id:"
echo $TF_VAR_folder_id
echo "----- Если id не пуст, то переменные окружения подгружены корректно."
echo ""

echo "--- Загрузка корневого сертификата для подключения к mqtt.cloud.yandex.net":
if [ ! -f rootCA.crt ]; then
  wget https://storage.yandexcloud.net/mqtt/rootCA.crt
  echo "----- Корневой сертификат загружен."
else
  echo "----- Корневой сертификат загружен ранее. Если срок действия истёк - удали его из данной директории и запусти скрипт заново."
fi
echo ""

echo "--- Создание пары ключей для устройств:"
if [ ! -f key.pm ] || [ ! -f cert.pem ]; then
  openssl req -x509 -newkey rsa:4096 -keyout key.pm -out cert.pem -nodes -days 365 -subj '/CN=localhost'
  echo "----- Ключи созданы."
else
  echo "----- Файлы key.pm и cert.pem уже существуют. Если срок действия истёк - удали их из данной директории и запусти скрипт заново."
fi

echo "--- Помещение пары ключей в переменные окружения"
export TF_VAR_device_public_certificate="$(cat cert.pem)"
export TF_VAR_device_secret_certificate="$(cat key.pm)"
echo ""

echo "--- Попытка удаления старых архивов collecting.zip и emulators.zip"
rm collecting.zip
rm emulators.zip
echo ""

cd ./collecting
echo "--- Создание zip-архива для Cloud Function collecting (сбор данных с IoT Core в S3)"
zip ../collecting  *
echo ""

cd ../emulators
echo "--- Создание zip-архива для Cloud Function emulators (эмуляция устройств)"
zip ../emulators  *
echo ""

cd ..
echo "--- Вычисление sha256-хэшей для архивов collecting.zip и emulators.zip"
export TF_VAR_collecting_hash="$(sha256sum collecting.zip)"
export TF_VAR_emulating_hash="$(sha256sum emulators.zip)"
echo ""

cd terraform
echo "--- Инициализация terraform..."
if [ -d .terraform ]; then
  echo "terraform init уже выполнена"
else
  terraform init
fi
echo ""

echo "--- Применение terraform apply"
terraform apply -auto-approve -parallelism=1