import re
import time

import pytest

from utils import weather


LAT = 55.752388  # Moscow latitude default
LON = 37.716457  # Moscow longitude default
TIME = int(time.time() - 3600)
PLACE = 'Moscow for test'

directions_to_try = [(0, 'N', 'С'), (7, 'N', 'С'), (11, 'N', 'С'), (12, 'NNE', 'ССВ'),
                     (33, 'NNE', 'ССВ'), (85, 'E', 'В'), (358, 'N', 'С'), (722, 'N', 'С')]
directions_ids = [f'{d[0]:<3}: {d[1]:>3}' for d in directions_to_try]


@pytest.mark.parametrize('degree, direction_en, direction_ru', directions_to_try, ids=directions_ids)
def test_compass_direction(degree, direction_en, direction_ru):
    """Should return correct direction in english and russian"""
    assert weather.compass_direction(degree) == direction_en
    assert weather.compass_direction(degree, 'ru') == direction_ru


def test_get_weather():
    descr = weather.get_weather('Some Place', LAT, LON)
    print('Description:\n', descr)
    assert re.fullmatch(r'🏙 Some Place: сейчас (\w+\s?){1,3}\n'
                        r'🌡 -?\d{1,2}(\.\d)?°C, ощущ. как -?\d{1,2}°C\n'
                        r'💨 \d{1,2}(\.\d)?м/с с.\w{1,3}, 💦.\d{1,3}%\n'
                        r'🌇 \d\d:\d\d ', descr)


def test_get_place_accu_params():
    place = weather.get_place_accu_params(LAT, LON)
    assert isinstance(place, str)
    assert re.fullmatch(r'https://www.accuweather.com/en/ru/\w+/(\d+)/weather-forecast/\1', place)


def test_get_air_quality():
    aqi, description = weather.get_air_quality('Test Place', LAT, LON, 'ru')
    print('Description:\n', description)
    print('AQI:', aqi)
    assert re.fullmatch(r'Test Place: воздух . PM2\.5~\d+, SO₂~\d+, NO₂~\d+, NH₃~\d+(\.\d)? \(в µg/m³\)\.', description)


def test_get_air_accu():
    url = 'https://www.accuweather.com/en/ru/lefortovo/589719/weather-forecast/589719'
    aqi, description = weather.get_air_accu(url)
    print(aqi, description)
    assert re.fullmatch(r'воздух .,( \d+\((O₃|PM2\.5|NO₂|SO₂|CO)\)-.,){5} в µg/m³\.', description)
    assert isinstance(aqi, int)
    assert 1 <= aqi <= 6
