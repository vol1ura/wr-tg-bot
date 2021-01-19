from dotenv import load_dotenv
import os
import requests
import time
from lxml.html import parse


def compass_direction(degree: int, lan='en') -> str:
    compass_arr = {'ru': ["С", "ССВ", "СВ", "ВСВ", "В", "ВЮВ", "ЮВ", "ЮЮВ",
                          "Ю", "ЮЮЗ", "ЮЗ", "ЗЮЗ", "З", "ЗСЗ", "СЗ", "ССЗ", "С"],
                   'en': ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                          "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW", "N"]}
    return compass_arr[lan][int((degree % 360) / 22.5 + 0.5)]


def get_weather(place, lat, lon, lang='ru'):
    weather_api_key = os.environ.get('OWM_TOKEN')
    base_url = f"http://api.openweathermap.org/data/2.5/weather?" \
               f"lat={lat}&lon={lon}&appid={weather_api_key}&units=metric&lang={lang}"
    w = requests.get(base_url).json()
    wind_dir = compass_direction(w['wind']['deg'], lang)
    sunset = time.strftime("%H:%M", time.localtime(w['sys']['sunset']))
    weather_desc = f"🏙 {place}: сейчас {w['weather'][0]['description']}\n" \
                   f"🌡 {w['main']['temp']:.1f}°C, ощущ. как {w['main']['feels_like']:.0f}°C\n" \
                   f"💨 {w['wind']['speed']:.1f}м/с с\xa0{wind_dir}, 💦\xa0{w['main']['humidity']}%\n" \
                   f"🌇 {sunset} "
    return weather_desc


def get_air_quality(place, lat, lon, lang='ru'):
    weather_api_key = os.environ.get('OWM_TOKEN')
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


pollutant = {'SO 2': 'SO₂', 'PM 2.5': 'PM2.5', 'O 3': 'O₃', 'PM 10': 'PM10', 'NO 2': 'NO₂', 'CO': 'CO'}
category = {'Fair': '🙂', 'Excellent': '👍', 'Poor': '😐', 'Unhealthy': '🙁', 'Very Unhealthy': '🤢', 'Dangerous': '☠'}
air_index = {'Fair': 2, 'Excellent': 1, 'Poor': 3, 'Unhealthy': 4, 'Very Unhealthy': 5, 'Dangerous': 6}


def get_air_accu(lat, lon):
    url = f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?" \
          f"apikey={os.environ.get('ACCW_KEY')}&q={lat}%2C{lon}&language=ru-ru"
    result = requests.get(url).json()
    key = result['Key']
    name = result['EnglishName']
    url = f'https://www.accuweather.com/en/ru/{name}/{key}/air-quality-index/{key}'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Host": "www.accuweather.com",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    }
    result = requests.get(url, headers=headers, stream=True)
    result.raw.decode_content = True
    tree = parse(result.raw)
    aqi_category = tree.xpath('//*/p[@class="category-text"]')[0].text_content().strip()
    air_description = f'воздух {category[aqi_category]}'
    rows = tree.xpath('//div[contains(@class, "air-quality-pollutant")]')
    for row in rows:
        p = row.xpath('.//div[@class="display-type"]')[0].text_content().strip()
        if p[-1] == '0':
            continue
        cat = row.xpath('.//div[@class="category"]')[0].text_content().strip()
        v_aqp = row.xpath('.//div[@class="pollutant-concentration"]')[0].text_content().split()[0]
        air_description += f', {v_aqp}({pollutant[p]}) {category[cat]}'
    air_description += ', в µg/m³.'
    return air_index[aqi_category], air_description


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    lat = 54.045048
    lon = 37.507175
    print(get_air_accu(lat, lon))
    # w = get_weather('Test', 43.585472, 39.723089)
    # print(w)
    # a = get_air_quality('Some place', 43.585472, 39.723089)
    # print(a[1])
