import math
import random
from datetime import datetime
import pytz

timezone = pytz.timezone("Europe/Moscow")

class Sensor:
    class EnvironmentalSensor:
        class Temperature:
            def __init__(self, sensor_amount = 1, 
                         annual_min = -5, 
                         annual_amp = 15, daily_amp = 3, 
                         annual_phase = 130, daily_phase = 6, 
                         gauss_multiplier = 3, gauss_mu = 0, gauss_sigma = 1):
                self.sensor_amount = sensor_amount
                self.annual_min = annual_min
                self.annual_amp = annual_amp
                self.daily_amp = daily_amp
                self.annual_phase = annual_phase
                self.daily_phase = daily_phase
                self.gauss_multiplier = gauss_multiplier
                self.gauss_mu = gauss_mu
                self.gauss_sigma = gauss_sigma

            def get_value(self, timestamp):
                annual_correction = self.annual_amp * math.sin(2 * math.pi * ((timestamp-self.annual_phase*86400) / (365*86400)))
                daily_correction = self.daily_amp * math.sin(2 * math.pi * (timestamp - self.daily_phase*3600) / 86400)
                gauss_correction = self.gauss_multiplier * random.gauss(self.gauss_mu, self.gauss_sigma)
                
                value = self.annual_min + annual_correction + daily_correction + gauss_correction
                return value

            def get_values(self, time = datetime.now(timezone)):
                year = time.year

                start_of_year = timezone.localize(datetime(year, 1, 1))
                delta = time.timestamp() - start_of_year.timestamp()

                return [self.get_value(delta) for _ in range(self.sensor_amount)]
            
        class Humidity:
            def __init__(self, sensor_amount = 1, gauss_mu = 60, gauss_sigma = 15):
                self.sensor_amount = sensor_amount
                self.gauss_mu = gauss_mu
                self.gauss_sigma = gauss_sigma
            
            def get_value(self):
                value = max(0, min(100, random.gauss(60, 15)))
                return value
            
            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]
            
        class AirQuality:
            def __init__(self, sensor_amount=1, base_aqi=50, sigma=10):
                self.sensor_amount = sensor_amount
                self.base_aqi = base_aqi
                self.sigma = sigma

            def get_value(self):
                return max(0, min(500, random.gauss(self.base_aqi, self.sigma)))

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class CO2:
            def __init__(self, sensor_amount=1, base_ppm=400, sigma=50):
                self.sensor_amount = sensor_amount
                self.base_ppm = base_ppm
                self.sigma = sigma

            def get_value(self):
                return max(300, random.gauss(self.base_ppm, self.sigma))

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class Light:
            def __init__(self, sensor_amount=1, max_lux=1000):
                self.sensor_amount = sensor_amount
                self.max_lux = max_lux

            def get_value(self, time):
                hour = time.hour
                factor = max(0, math.sin(hour * math.pi / 12))
                return random.uniform(0.8, 1.2) * self.max_lux * factor

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value(time) for _ in range(self.sensor_amount)]

        class Noise:
            def __init__(self, sensor_amount=1, base_db=40, sigma=10):
                self.sensor_amount = sensor_amount
                self.base_db = base_db
                self.sigma = sigma

            def get_value(self):
                return max(0, random.gauss(self.base_db, self.sigma))

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class WindSpeed:
            def __init__(self, sensor_amount=1, max_speed=20):
                self.sensor_amount = sensor_amount
                self.max_speed = max_speed

            def get_value(self):
                return max(0, random.gauss(5, 3))

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class WindDirection:
            def __init__(self, sensor_amount=1):
                self.sensor_amount = sensor_amount

            def get_value(self):
                return random.uniform(0, 360)

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class Rainfall:
            def __init__(self, sensor_amount=1, chance=0.3, max_mm=20):
                self.sensor_amount = sensor_amount
                self.chance = chance
                self.max_mm = max_mm

            def get_value(self):
                return random.uniform(0, self.max_mm) if random.random() < self.chance else 0.0

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class Pressure:
            def __init__(self, sensor_amount=1, base_hpa=1013, sigma=10):
                self.sensor_amount = sensor_amount
                self.base_hpa = base_hpa
                self.sigma = sigma

            def get_value(self):
                return random.gauss(self.base_hpa, self.sigma)

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

    class LocationSensor:
        class GPS:
            def __init__(self, sensor_amount=1, base_lat=59.9386, base_lon=30.3141, delta=0.01):
                self.sensor_amount = sensor_amount
                self.base_lat = base_lat
                self.base_lon = base_lon
                self.delta = delta

            def get_value(self):
                return {
                    "latitude": self.base_lat + random.uniform(-self.delta, self.delta),
                    "longitude": self.base_lon + random.uniform(-self.delta, self.delta)
                }

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

    class PowerSensor:
        class Voltage:
            def __init__(self, sensor_amount=1, base_volts=220, sigma=5):
                self.sensor_amount = sensor_amount
                self.base_volts = base_volts
                self.sigma = sigma

            def get_value(self):
                return random.gauss(self.base_volts, self.sigma)

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class Current:
            def __init__(self, sensor_amount=1, base_amperes=5, sigma=1):
                self.sensor_amount = sensor_amount
                self.base_amperes = base_amperes
                self.sigma = sigma

            def get_value(self):
                return max(0, random.gauss(self.base_amperes, self.sigma))

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]

        class PowerConsumption:
            def __init__(self, sensor_amount=1):
                self.sensor_amount = sensor_amount
                self.voltage_sensor = Sensor.PowerSensor.Voltage()
                self.current_sensor = Sensor.PowerSensor.Current()

            def get_value(self):
                voltage = self.voltage_sensor.get_value()
                current = self.current_sensor.get_value()
                return voltage * current

            def get_values(self, time = datetime.now(timezone)):
                return [self.get_value() for _ in range(self.sensor_amount)]