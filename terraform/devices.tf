# Тестовые устройства
variable "devices" {
  type = map(object({
    description = string
    class       = string
    type        = string
    amount      = number
  }))
  default = {
    environmental-temperature-device-1 = { description = "Тестовый датчик температуры, передающий по одному показанию", class = "EnvironmentalSensor", type = "Temperature", amount = 1 }
    environmental-temperature-device-2 = { description = "Тестовый датчик температуры, передающий по три показания", class = "EnvironmentalSensor", type = "Temperature", amount = 2 }
    environmental-humidity-device-1 = { description = "Тестовый датчик влажности", class = "EnvironmentalSensor", type = "Humidity", amount = 1 }
    # environmental-airquality-device-1 = { description = "Тестовый датчик качества воздуха окружающей среды", class = "EnvironmentalSensor", type = "AirQuality", amount = 1 }
    # environmental-co2-device-1 = { description = "Тестовый датчик содержания CO2", class = "EnvironmentalSensor", type = "CO2", amount = 1 }
    # environmental-light-device-1 = { description = "Тестовый датчик уровня освещенности", class = "EnvironmentalSensor", type = "Light", amount = 1 }
    # environmental-noise-device-1 = { description = "Тестовый датчик уровня шума", class = "EnvironmentalSensor", type = "Noise", amount = 1 }
    # environmental-windspeed-device-1 = { description = "Тестовый датчик скорости ветра", class = "EnvironmentalSensor", type = "WindSpeed", amount = 1 }
    # environmental-winddirection-device-1 = { description = "Тестовый датчик направления ветра", class = "EnvironmentalSensor", type = "WindDirection", amount = 1 }
    # environmental-rainfall-device-1 = { description = "Тестовый датчик количества осадков", class = "EnvironmentalSensor", type = "Rainfall", amount = 1 }
    # environmental-pressure-device-1 = { description = "Тестовый датчик давления", class = "EnvironmentalSensor", type = "Pressure", amount = 1 }
    location-gps-device-1 = { description = "Тестовый датчик местоположения", class = "LocationSensor", type = "GPS", amount = 1 }
    power-voltage-device-1 = { description = "Тестовый датчик напряжения", class = "PowerSensor", type = "Voltage", amount = 1 }
    power-current-device-1 = { description = "Тестовый датчик тока", class = "PowerSensor", type = "Current", amount = 1 }
    power-powerconsumption-device-1 = { description = "Тестовый датчик мощности", class = "PowerSensor", type = "PowerConsumption", amount = 1 }
  }
}
