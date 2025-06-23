# Тестовые устройства
variable "devices" {
  type = map(object({
    description = string
  }))
  default = {
    environmental_temperature_device_1 = { description = "Тестовый датчик температуры, передающий по одному показанию", class = "EnvironmentalSensor", type = "Temperature", amount = 1 }
    environmental_temperature_device_2 = { description = "Тестовый датчик температуры, передающий по три показания", class = "EnvironmentalSensor", type = "Temperature", amount = 2 }
    environmental_humidity_device_1 = { description = "Тестовый датчик влажности", class = "EnvironmentalSensor", type = "Humidity", amount = 1 }
    environmental_airquality_device_1 = { description = "Тестовый датчик качества воздуха окружающей среды", class = "EnvironmentalSensor", type = "AirQuality", amount = 1 }
    environmental_co2_device_1 = { description = "Тестовый датчик содержания CO2", class = "EnvironmentalSensor", type = "CO2", amount = 1 }
    environmental_light_device_1 = { description = "Тестовый датчик уровня освещенности", class = "EnvironmentalSensor", type = "Light", amount = 1 }
    environmental_noise_device_1 = { description = "Тестовый датчик уровня шума", class = "EnvironmentalSensor", type = "Noise", amount = 1 }
    environmental_windspeed_device_1 = { description = "Тестовый датчик скорости ветра", class = "EnvironmentalSensor", type = "WindSpeed", amount = 1 }
    environmental_winddirection_device_1 = { description = "Тестовый датчик направления ветра", class = "EnvironmentalSensor", type = "WindDirection", amount = 1 }
    environmental_rainfall_device_1 = { description = "Тестовый датчик количества осадков", class = "EnvironmentalSensor", type = "Rainfall", amount = 1 }
    environmental_pressure_device_1 = { description = "Тестовый датчик давления", class = "EnvironmentalSensor", type = "Pressure", amount = 1 }
    location_gps_device_1 = { description = "Тестовый датчик местоположения", class = "LocationSensor", type = "GPS", amount = 1 }
    power_voltage_device_1 = { description = "Тестовый датчик напряжения", class = "PowerSensor", type = "Voltage", amount = 1 }
    power_current_device_1 = { description = "Тестовый датчик тока", class = "PowerSensor", type = "Current", amount = 1 }
    power_powerconsumption_device_1 = { description = "Тестовый датчик мощности", class = "PowerSensor", type = "PowerConsumption", amount = 1 }
  }
}
