terraform {
   required_providers {
     yandex = {
       source = "yandex-cloud/yandex"
     }
     tls = {
      source  = "hashicorp/tls"
    }
    local = {
      source = "hashicorp/local"
    }
   }
 }
  
provider "yandex" {
    token  =  var.token
    cloud_id  = var.cloud_id
    # folder_id = var.folder_id
    # zone      = "ru-central1-a"
}
 
//
// Create a new Folder.
//
resource "yandex_resourcemanager_folder" "folder" {
  name = var.iot_folder_name
  cloud_id = var.cloud_id
  description = "Каталог, созданный при помощи terraform для дипломной работы"
}

//
// Create a new IoT Core Registry.
//
resource "yandex_iot_core_registry" "registry" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  name        = var.iot_registry_name
  description = "Реестр устройств для выполнения дипломной работы"
}

//
// Simple Private Bucket With Static Access Keys.
//

// Create SA
resource "yandex_iam_service_account" "sa" {
  folder_id = yandex_resourcemanager_folder.folder.id
  name      = var.iot_sa_name
}

// Grant permissions
resource "yandex_resourcemanager_folder_iam_member" "sa-editor" {
  folder_id = yandex_resourcemanager_folder.folder.id
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "trigger-editor" {
  folder_id = yandex_resourcemanager_folder.folder.id
  role      = "functions.editor"
  member    = "serviceAccount:${yandex_iam_service_account.sa.id}"
}

// Create Static Access Keys
resource "yandex_iam_service_account_static_access_key" "sa-static-key" {
  service_account_id = yandex_iam_service_account.sa.id
  description        = "Статичный access-key для аккаунта ${var.iot_sa_name}"
}

// Use keys to create bucket
resource "yandex_storage_bucket" "bucket" {
  folder_id  = yandex_resourcemanager_folder.folder.id
  access_key = yandex_iam_service_account_static_access_key.sa-static-key.access_key
  secret_key = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
  bucket     = var.iot_bucket_name
}

//
//  Generate certificates for devices
//

// Generate private keys
resource "tls_private_key" "device_keys" {
  for_each = var.devices

  algorithm = "RSA"
  rsa_bits  = 2048
}

// Generate public certificates
resource "tls_self_signed_cert" "device_certs" {
  for_each = var.devices

  private_key_pem = tls_private_key.device_keys[each.key].private_key_pem

  subject {
    common_name = each.key
  }

  validity_period_hours = 8760  # 1 год
  is_ca_certificate     = false

  allowed_uses = [
    "digital_signature",
    "key_encipherment",
    "server_auth",
    "client_auth",
  ]
}

// Write to files
resource "local_file" "cert_files" {
  for_each = var.devices

  content  = tls_self_signed_cert.device_certs[each.key].cert_pem
  filename = "${path.module}/../certificates/${each.key}.crt"
}

resource "local_file" "key_files" {
  for_each = var.devices

  content  = tls_private_key.device_keys[each.key].private_key_pem
  filename = "${path.module}/../certificates/${each.key}.key"
}


//
// Create a new IoT Core Device.
//
resource "yandex_iot_core_device" "device" {
  for_each    = var.devices

  registry_id = yandex_iot_core_registry.registry.id
  name        = each.key
  description = each.value.description
  certificates = [
    tls_self_signed_cert.device_certs[each.key].cert_pem
  ]
}

//
// Create a new Yandex Cloud Function
//
resource "yandex_function" "collecting-function" {
  folder_id          = yandex_resourcemanager_folder.folder.id
  name               = var.iot_collecting_function_name
  description        = "Cloud Function, вызываемая по триггеру из реестра ${var.iot_collecting_function_name} и сохраняющая данные в бакет ${var.iot_bucket_name}"
  user_hash          = var.collecting_hash
  runtime            = "python312"
  entrypoint         = "index.handler"
  memory             = "256"
  execution_timeout  = "10"
  service_account_id = yandex_iam_service_account.sa.id
  # todo переделать на secrets, если будет время
  environment = {
    ACCESS_KEY  = yandex_iam_service_account_static_access_key.sa-static-key.access_key
    SECRET_KEY  = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
    BUCKET_NAME = var.iot_bucket_name
  }
  content {
    zip_filename = "../collecting.zip"
  }
}

//
// Create a new Cloud Function Trigger.
//
resource "yandex_function_trigger" "collecting-trigger" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  name        = var.iot_collecting_trigger_name
  description = "Триггер, вызывающий функцию ${var.iot_collecting_function_name}, которая сохраняет данные из устройств реестра ${var.iot_registry_name} в бакет ${var.iot_bucket_name}"
  iot {
    batch_cutoff    = 0
    registry_id     = yandex_iot_core_registry.registry.id
  }
  function {
    id                  = yandex_function.collecting-function.id
    service_account_id  = yandex_iam_service_account.sa.id
  }
}

//
// Generate zip archives with emulators
//

data "local_file" "emulator_py" {
  filename = "${path.module}/../emulators/emulator.py"
}

data "local_file" "config_py" {
  filename = "${path.module}/../emulators/config.py"
}

data "local_file" "main_py" {
  filename = "${path.module}/../emulators/main.py"
}

data "local_file" "sender_py" {
  filename = "${path.module}/../emulators/sender.py"
}

data "local_file" "rootCA" {
  filename = "${path.module}/../certificates/rootCA.crt"
}

data "local_file" "requirements_txt" {
  filename = "${path.module}/../emulators/requirements.txt"
}


resource "archive_file" "emulators_archives" {
  for_each = var.devices

  type        = "zip"
  output_path = "${path.module}/../emulators-build/${each.key}.zip"

  source {
    content  = tls_private_key.device_keys[each.key].private_key_pem
    filename = "key.pm"
  }

  source {
    content  = tls_self_signed_cert.device_certs[each.key].cert_pem
    filename = "cert.pem"
  }

  source {
    content  = data.local_file.emulator_py.content
    filename = "emulator.py"
  }

  source {
    content  = data.local_file.config_py.content
    filename = "config.py"
  }

  source {
    content  = data.local_file.main_py.content
    filename = "main.py"
  }

  source {
    content  = data.local_file.sender_py.content
    filename = "sender.py"
  }

  source {
    content  = data.local_file.requirements_txt.content
    filename = "requirements.txt"
  }

  source {
    content  = data.local_file.rootCA.content
    filename = "rootCA.crt"
  }

}

//
// Create a new Yandex Cloud Function (emulators)
//
resource "yandex_function" "emulating-functions" {
  for_each = var.devices
  
  folder_id          = yandex_resourcemanager_folder.folder.id
  name               = "${var.iot_emulating_function_name}-${each.key}"
  description        = "Cloud Function, эмулирующая поведение устройства ${each.key}"
  user_hash          = archive_file.emulators_archives[each.key].output_sha256
  runtime            = "python312"
  entrypoint         = "main.handler"
  memory             = "256"
  execution_timeout  = "10"
  service_account_id = yandex_iam_service_account.sa.id
  # todo переделать на secrets, если будет время
  environment = {
    DEVICE_ID         = yandex_iot_core_device.device[each.key].id
    SENSORS_CLASSES   = each.value.class
    SENSORS_TYPES     = each.value.type
    SENSORS_IDS       = each.value.sensorid
    TIME_TO_EMULATE   = "NOW"
  }
  content {
    zip_filename = "../emulators-build/${each.key}.zip"
  }
}

//
// Create a new Cloud Function Trigger.  (emulators)
//
resource "yandex_function_trigger" "emulators-trigger" {
  for_each = var.devices
  
  folder_id   = yandex_resourcemanager_folder.folder.id
  name        = "${var.iot_emulating_trigger_name}-${each.key}"
  description = "Триггер, вызывающий функцию ${var.iot_emulating_function_name}-${each.key}, эмулирующая устройство"
  timer {
    cron_expression = "* * * * ? *"
  }
  function {
    id                  = yandex_function.emulating-functions[each.key].id
    service_account_id  = yandex_iam_service_account.sa.id
  }
}

//
// Create a new MDB PostgreSQL Database.
//
resource "yandex_mdb_postgresql_database" "my_db" {
  cluster_id = yandex_mdb_postgresql_cluster.my_cluster.id
  name       = var.iot_database_name
  owner      = yandex_mdb_postgresql_user.my_user.name
  lc_collate = "en_US.UTF-8"
  lc_type    = "en_US.UTF-8"
  extension {
    name = "uuid-ossp"
  }
  extension {
    name = "xml2"
  }
}

resource "yandex_mdb_postgresql_user" "my_user" {
  cluster_id = yandex_mdb_postgresql_cluster.my_cluster.id
  name       = var.iot_database_user
  password   = var.iot_database_password
}

resource "yandex_mdb_postgresql_cluster" "my_cluster" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  name        = var.iot_database_cluster_name
  environment = "PRESTABLE"
  network_id  = yandex_vpc_network.foo.id

  config {
    version = 15
    resources {
      resource_preset_id = "c3-c2-m4"
      disk_type_id       = "network-ssd"
      disk_size          = 10
    }
  }

  host {
    assign_public_ip = true
    zone      = "ru-central1-d"
    subnet_id = yandex_vpc_subnet.foo.id
  }
}

// Auxiliary resources
resource "yandex_vpc_network" "foo" {
  folder_id   = yandex_resourcemanager_folder.folder.id
}

resource "yandex_vpc_subnet" "foo" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  zone           = "ru-central1-d"
  network_id     = yandex_vpc_network.foo.id
  v4_cidr_blocks = ["10.5.0.0/24"]
}

resource "yandex_vpc_subnet" "foo_compute_instance" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.foo.id
  v4_cidr_blocks = ["10.4.0.0/24"]
}

//
// Create a new Yandex Cloud Function (averaging)
//
resource "yandex_function" "averaging-function" {
  folder_id          = yandex_resourcemanager_folder.folder.id
  name               = var.iot_averaging_function_name
  description        = "Cloud Function, вызываемая по триггеру ${var.iot_averaging_trigger_name} и усредняющая данные"
  user_hash          = var.averaging_hash
  runtime            = "python312"
  entrypoint         = "index.handler"
  memory             = "1024"
  execution_timeout  = "600"
  service_account_id = yandex_iam_service_account.sa.id
  # todo переделать на secrets, если будет время
  environment = {
    ACCESS_KEY  = yandex_iam_service_account_static_access_key.sa-static-key.access_key
    SECRET_KEY  = yandex_iam_service_account_static_access_key.sa-static-key.secret_key
    BUCKET_NAME = var.iot_bucket_name
    DB_DSN      = "postgresql://${var.iot_database_user}:${var.iot_database_password}@${yandex_mdb_postgresql_cluster.my_cluster.host[0].fqdn}:6432/${var.iot_database_name}"
  }
  content {
    zip_filename = "../averaging.zip"
  }
}

//
// Create a new Cloud Function Trigger (averaging)
//
resource "yandex_function_trigger" "averaging-trigger" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  name        = var.iot_averaging_trigger_name
  description = "Триггер, вызывающий функцию ${var.iot_averaging_function_name}, которая усредняет данные"
  timer {
    cron_expression = "*/10 * * * ? *"
  }
  function {
    id                  = yandex_function.averaging-function.id
    service_account_id  = yandex_iam_service_account.sa.id
  }
}

//
// Create a new VPC regular IPv4 Address.
//
resource "yandex_vpc_address" "addr" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  name = var.iot_vpc_static_address

  external_ipv4_address {
    zone_id = "ru-central1-b"
  }
}

//
// Create a new Compute Disk.
//
resource "yandex_compute_disk" "my_disk" {
  name     = var.iot_cloud_disk_name
  size = 10
  zone = "ru-central1-b"
  folder_id   = yandex_resourcemanager_folder.folder.id
  type     = "network-ssd"
  image_id = "fd80j21lmqard15ciskf"  # ubuntu 24.04
}

//
// Create a new Compute Instance
//
resource "yandex_compute_instance" "default" {
  folder_id   = yandex_resourcemanager_folder.folder.id
  name        = var.iot_cloud_instance_name
  zone = "ru-central1-b"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    disk_id = yandex_compute_disk.my_disk.id
  }

  network_interface {
    nat       = true
    subnet_id = yandex_vpc_subnet.foo_compute_instance.id
    nat_ip_address = yandex_vpc_address.addr.external_ipv4_address[0].address
  }

  metadata = {
    user-data = "${file("../grafana/cloud-init.yaml")}"
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}