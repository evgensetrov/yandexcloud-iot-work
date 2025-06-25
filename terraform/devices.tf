# Тестовые устройства
variable "devices" {
  type = map(object({
    description = string
    class       = string
    type        = string
    sensorid    = string
  }))
  default = {
    device-1 = { 
      description = "Тестовое устройство с одним датчиком температуры", 
      class = "['EnvironmentalSensor']", 
      type = "['Temperature']", 
      sensorid = "['75dc5f0c-4320-4a88-8e9e-5fdd6aa77ec1']"
    }
    device-2 = {
      description = "Тестовое устройство с датчиком температуры, влажности, освещенности и шума", 
      class = "['EnvironmentalSensor', 'EnvironmentalSensor', 'EnvironmentalSensor', 'EnvironmentalSensor']", 
      type = "['Temperature', 'Humidity', 'Light', 'Noise']", 
      sensorid = "['91d92bc4-a5cc-49a8-a761-d20125737554', '459054ca-92a9-4b7b-b5d4-fe1e0ff028ec', '45c67c2b-59c6-40f6-b652-b680b340d7b3', '8378d12b-693a-4b54-9485-a1072313a331']"
    }
    device-4 = {
      description = "Тестовое устройство с датчиками напряжения, тока и мощности",
      class = "['PowerSensor', 'PowerSensor', 'PowerSensor']"
      type = "['Voltage' ,'Current' ,'PowerConsumption']"
      sensorid = "['04230ee1-ed91-4ad9-a493-5374edcce75a' ,'aa887811-61fa-48be-8fc4-a7038527df8e' ,'bdace89c-be4e-4dae-b2aa-0508e9766192']"
    }
  }
}
