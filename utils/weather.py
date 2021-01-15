import requests
import time

import config


def compass_direction(degree: int, lan='en') -> str:
    compass_arr = {'ru': ["С", "ССВ", "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ",
                          "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ", "С"],
                   'en': ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]}
    return compass_arr[lan][int((degree % 360) / 22.5 + 0.5)]


def get_weather(place, lat, lon, lang='ru'):
    weather_api_key = config.OWM_TOKEN
    base_url = f"http://api.openweathermap.org/data/2.5/weather?" \
               f"lat={lat}&lon={lon}&appid={weather_api_key}&units=metric&lang={lang}"
    w = requests.get(base_url).json()
    # TODO Add rain and snow volume
    wind_dir = compass_direction(w['wind']['deg'], lang)
    sunset = time.strftime("%H:%M", time.localtime(w['sys']['sunset']))
    weather_desc = f"🏙 {place}: сейчас {w['weather'][0]['description']} \n" \
                   f"🌡 {w['main']['temp']:.1f}°C, ощущ. как {w['main']['feels_like']:.0f}°C\n" \
                   f"💨 {w['wind']['speed']:.1f}м/с с {wind_dir}, 💦 {w['main']['humidity']}%\n" \
                   f"🌇 {sunset}   "
    return weather_desc


def get_air_quality(place, lat, lon, lang='ru'):
    weather_api_key = config.OWM_TOKEN
    base_url = f"http://api.openweathermap.org/data/2.5/air_pollution?" \
               f"lat={lat}&lon={lon}&appid={weather_api_key}"
    aq = requests.get(base_url).json()
    # Air Quality Index: 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor
    aqi = aq['list'][0]['main']['aqi']
    aqi_e = ['👍', '🙂', '😐', '🙁', '🤢'][aqi - 1]
    air = {'ru': 'воздух', 'en': 'air'}
    air_conditions = f"{place}: {air[lang]} {aqi_e} {aq['list'][0]['components']['so2']}(PM2.5), " \
                     f"{aq['list'][0]['components']['so2']}(SO₂), {aq['list'][0]['components']['no2']}(NO₂), " \
                     f"{aq['list'][0]['components']['nh3']}(NH₃)."
    return aqi, air_conditions


if __name__ == '__main__':
    w = get_weather(43.585472, 39.723089)
    print(w)
    a = get_air_quality(43.585472, 39.723089)
    print(a[1])
