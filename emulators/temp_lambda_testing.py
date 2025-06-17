import math
import random
from datetime import datetime, timedelta
import pandas as pd

def temperature_spb(t):
    annual = 5 + 15 * math.sin(2 * math.pi * (t - 200*86400 / (365 * 86400)))
    daily = 3 * math.sin(2 * math.pi * (t % 86400) / 86400)
    noise = random.gauss(0, 0.7)
    return round(annual + daily + noise, 2)

dates_to_check = [
    ("Январь", 1), ("Февраль", 3), ("Март", 2),
    ("Апрель", 5), ("Май", 13), ("Июнь", 6),
    ("Июль", 30), ("Август", 2), ("Сентябрь", 17),
    ("Октябрь", 27), ("Ноябрь", 16), ("Декабрь", 4)
]

# Времена суток
times_of_day = [("00:00", 0), ("06:00", 6), ("12:00", 12), ("18:00", 18)]

# Базовая дата начала года
year_start = datetime(year=2025, month=1, day=1)

results = []

# Посчитаем температуру для всех комбинаций
for month_name, day in dates_to_check:
    month_index = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                   "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"].index(month_name) + 1
    for time_label, hour in times_of_day:
        try:
            dt = datetime(2025, month_index, day, hour, 0)
            t = (dt - year_start).total_seconds()
            temp = temperature_spb(t)
            results.append({
                "Месяц": month_name,
                "День": day,
                "Время": time_label,
                "Температура (°C)": temp
            })
        except Exception as e:
            results.append({
                "Месяц": month_name,
                "День": day,
                "Время": time_label,
                "Температура (°C)": f"Ошибка: {e}"
            })

df = pd.DataFrame(results)
df_pivot = df.pivot(index=["Месяц", "День"], columns="Время", values="Температура (°C)")
print(df)