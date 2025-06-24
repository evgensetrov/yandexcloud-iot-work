import math
import random
from datetime import datetime
import pytz

timezone = pytz.timezone("Europe/Moscow")

class Sensor:
    class EnvironmentalSensor:
        class Temperature:
            def __init__(self, 
                         annual_min = -5, 
                         annual_amp = 15, daily_amp = 3, 
                         annual_phase = 130, daily_phase = 6, 
                         gauss_multiplier = 3, gauss_mu = 0, gauss_sigma = 1):
                self.annual_min = annual_min
                self.annual_amp = annual_amp
                self.daily_amp = daily_amp
                self.annual_phase = annual_phase
                self.daily_phase = daily_phase
                self.gauss_multiplier = gauss_multiplier
                self.gauss_mu = gauss_mu
                self.gauss_sigma = gauss_sigma

            def get_value_delta(self, timestamp):
                annual_correction = self.annual_amp * math.sin(2 * math.pi * ((timestamp-self.annual_phase*86400) / (365*86400)))
                daily_correction = self.daily_amp * math.sin(2 * math.pi * (timestamp - self.daily_phase*3600) / 86400)
                gauss_correction = self.gauss_multiplier * random.gauss(self.gauss_mu, self.gauss_sigma)
                
                value = self.annual_min + annual_correction + daily_correction + gauss_correction
                return value

            def get_value(self, time = datetime.now(timezone)):
                year = time.year

                start_of_year = timezone.localize(datetime(year, 1, 1))
                delta = time.timestamp() - start_of_year.timestamp()

                return self.get_value_delta(delta)
            
        class Humidity:
            def __init__(self, gauss_mu = 60, gauss_sigma = 15):
                self.gauss_mu = gauss_mu
                self.gauss_sigma = gauss_sigma
            
            def get_value(self, time = datetime.now(timezone)):
                value = max(0, min(100, random.gauss(60, 15)))
                return value
            
        class AirQuality:
            def __init__(self, base_aqi=50, sigma=10):
                self.base_aqi = base_aqi
                self.sigma = sigma

            def get_value(self, time = datetime.now(timezone)):
                return max(0, min(500, random.gauss(self.base_aqi, self.sigma)))

        class CO2:
            def __init__(self, base_ppm=400, sigma=50):
                self.base_ppm = base_ppm
                self.sigma = sigma

            def get_value(self, time = datetime.now(timezone)):
                return max(300, random.gauss(self.base_ppm, self.sigma))

        class Light:
            def __init__(self, max_lux=1000):
                self.max_lux = max_lux

            def get_value(self, time = datetime.now(timezone)):
                hour = time.hour
                factor = max(0.1, math.sin(hour * math.pi / 12))
                return random.uniform(0.8, 1.2) * self.max_lux * factor

        class Noise:
            def __init__(self, base_db=40, sigma=10):
                self.base_db = base_db
                self.sigma = sigma

            def get_value(self, time = datetime.now(timezone)):
                return max(0, random.gauss(self.base_db, self.sigma))

        class WindSpeed:
            def __init__(self, max_speed=20):
                self.max_speed = max_speed

            def get_value(self, time = datetime.now(timezone)):
                return max(0, random.gauss(5, 3))

        class WindDirection:
            def __init__(self):
                pass

            def get_value(self, time = datetime.now(timezone)):
                return random.uniform(0, 360)

        class Rainfall:
            def __init__(self, chance=0.3, max_mm=20):
                self.chance = chance
                self.max_mm = max_mm

            def get_value(self, time = datetime.now(timezone)):
                return random.uniform(0, self.max_mm) if random.random() < self.chance else 0.0

        class Pressure:
            def __init__(self, base_hpa=1013, sigma=10):
                self.base_hpa = base_hpa
                self.sigma = sigma

            def get_value(self, time = datetime.now(timezone)):
                return random.gauss(self.base_hpa, self.sigma)

    class LocationSensor:
        class GPS:
            def __init__(self, base_lat=59.9386, base_lon=30.3141, delta=0.01):
                self.base_lat = base_lat
                self.base_lon = base_lon
                self.delta = delta

            def get_value(self, time = datetime.now(timezone)):
                return {
                    "latitude": self.base_lat + random.uniform(-self.delta, self.delta),
                    "longitude": self.base_lon + random.uniform(-self.delta, self.delta)
                }

    class PowerSensor:
        class Voltage:
            def __init__(self, base_volts=220, sigma=5):
                self.base_volts = base_volts
                self.sigma = sigma

            def get_value(self, time = datetime.now(timezone)):
                return random.gauss(self.base_volts, self.sigma)

        class Current:
            def __init__(self, base_amperes=5, sigma=1):
                self.base_amperes = base_amperes
                self.sigma = sigma

            def get_value(self, time = datetime.now(timezone)):
                return max(0, random.gauss(self.base_amperes, self.sigma))

        class PowerConsumption:
            def __init__(self):
                self.voltage_sensor = Sensor.PowerSensor.Voltage()
                self.current_sensor = Sensor.PowerSensor.Current()

            def get_value(self, time = datetime.now(timezone)):
                voltage = self.voltage_sensor.get_value()
                current = self.current_sensor.get_value()
                return voltage * current