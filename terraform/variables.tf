variable "token" {
    type = string
    default = ""  # пустое, т.к. используем переменную окружения TF_VAR_token, перехватываемую terraform-ом
}

variable "cloud_id" {
    type = string
    default = ""
}

variable "iot_folder_name" {
    type = string
    default = "iot-folder-spring2025"
}

variable "iot_registry_name" {
    type = string
    default = "iot-registry-spring2025"
}

variable "iot_bucket_name" {
    type = string
    default = "iot-bucket-spring2025"
}

variable "iot_sa_name" {  # сервисный аккаунт
    type = string
    default = "iot-sa-spring2025"
}

variable "iot_collecting_function_name" {
    type = string
    default = "iot-collecting-function-spring2025"
}

variable "iot_collecting_trigger_name" {
    type = string
    default = "iot-collecting-trigger-spring2025"
}

variable "iot_averaging_function_name" {
    type = string
    default = "iot-averaging-function-spring2025"
}

variable "iot_averaging_trigger_name" {
    type = string
    default = "iot-averaging-trigger-spring2025"
}

variable "iot_emulating_function_name" {
    type = string
    default = "emufunc"
}

variable "iot_emulating_trigger_name" {
    type = string
    default = "emutrig"
}

variable "iot_database_cluster_name" {
    type = string
    default = "iot_database_cluster"
}

variable "iot_database_name" {
    type = string
    default = "iot"
}

variable "iot_database_user" {
    type = string
    default = ""
}

variable "iot_database_password" {
    type = string
    default = ""
}

variable "iot_cloud_disk_name" {
    type = string
    default = "iot-grafana-disk"
}

variable "iot_vpc_static_address" {
    type = string
    default = "iot-grafana-ip"
}

variable "iot_cloud_instance_name" {
    type = string
    default = "iot-grafana"
}


variable "collecting_hash" {
    type = string
    default = ""
}

variable "averaging_hash" {
    type = string
    default = ""
}
