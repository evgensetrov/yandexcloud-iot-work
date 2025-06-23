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


variable "iot_emulating_function_name" {
    type = string
    default = "iot-emulating-function-spring2025"
}

variable "collecting_hash" {
    type = string
    default = ""
}

variable "emulating_hash" {
    type = string
    default = ""
}
