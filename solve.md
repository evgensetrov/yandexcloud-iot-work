Результат сканирования портов matt.cloud.yandex.net:
```
root@evgeniy-note:/mnt/c/Users/evgen# nmap -p1-10000 mqtt.cloud.yandex.net
Starting Nmap 7.95 ( https://nmap.org ) at 2025-06-17 19:30 MSK
Nmap scan report for mqtt.cloud.yandex.net (130.193.44.244)
Host is up (0.023s latency).
Not shown: 9999 filtered tcp ports (no-response)
PORT     STATE SERVICE
8883/tcp open  secure-mqtt

Nmap done: 1 IP address (1 host up) scanned in 390.58 seconds
```

-> открыт только 8883 порт, доступ видимо только по сертификатам.

## 0. Создание эмуляторов
1) Создание сертификата:
```
openssl req -x509 -newkey rsa:4096 -keyout key.pm -out cert.pem -nodes -days 365 -subj '/CN=localhost'
```

(см. https://yandex.cloud/ru/docs/iot-core/operations/certificates/create-certificates)

2) Добавление сертификата к устройству:
```
yc iot device certificate add --device-name test-device --certificate-file cert.pem
```

3) Проверка сертификатов:
```
yc iot device certificate list --device-name test-device
```
(см. https://yandex.cloud/ru/docs/iot-core/operations/certificates/device-certificates)

4) Качаем корневой сертификат УЦ от Яндекса:
```
wget https://storage.yandexcloud.net/mqtt/rootCA.crt
```

5) Отправка тестов при помощи mosquitto_pub:
```
mosquitto_pub -h mqtt.cloud.yandex.net -p 8883 --cafile rootCA.crt --cert cert.pem --key key.pm  -t '$devices/are8mjfvrc1ffara02di/events' -m 'Test data' -q 1
```

## 2. Хранение в Object Storage
Создание access key:
```
yc iam access-key create --service-account-name test

access_key:
  id: ajefjkrpcft31jc4v85p
  service_account_id: ajecae7ilhh246bh6vjg
  created_at: "2025-06-17T17:15:41.504473491Z"
  key_id: YCAJEui0jtw9TXTBU2Q-gVKTH
secret: YCNiemeT49cwCnCgtKkWM8jXZRWzvgU09xpuNtbL
```

Создание функции: см. **collecting.**
Пример передаваемого триггером event:
```
{
  "messages": [
    {
      "event_metadata": {
        "event_id": "1849e505535fea2f00",
        "event_type": "yandex.cloud.events.iot.IoTMessage",
        "created_at": "2025-06-17T17:35:41.246540335Z",
        "folder_id": "b1ggu7a1ui4o4r14gug7"
      },
      "details": {
        "registry_id": "arekf2gmdu9mek1m455e",
        "device_id": "are8mjfvrc1ffara02di",
        "mqtt_topic": "$devices/are8mjfvrc1ffara02di/events",
        "payload": "VGVzdCBkYXRh"
      }
    }
  ]
}
```
**payload** - в base64.

