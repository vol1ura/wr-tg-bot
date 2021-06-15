import os
import re
from datetime import date
from time import sleep

import pandas
import pytest
import requests
import responses
from lxml.html import fromstring

from utils import parkrun
from utils.parkrun import parkrun_headers


class ParkrunMock:
    PARKRUN_PAGES = {
        'consolidatedclub': 'https://www.parkrun.com/results/consolidatedclub/?clubNum=23212',
        'clubhistory': 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212',
        'courserecords': 'https://www.parkrun.ru/results/courserecords/'
    }

    def __init__(self, page):
        self.__page = page
        self.__page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'content/{page}.html')
        if not os.path.exists(self.__page_path):
            self.__prepare_results()

    def read_content(self):
        with open(self.__page_path) as f:
            return f.read()

    def get_html_tree(self, _):
        return fromstring(self.read_content())

    def __prepare_results(self):
        sleep(1.5)
        result = requests.get(ParkrunMock.PARKRUN_PAGES[self.__page], headers=parkrun_headers)
        with open(self.__page_path, 'w') as f:
            f.write(result.text)


@pytest.fixture
def clubhistory_mock():
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    responses.add(responses.GET, url, body=ParkrunMock('clubhistory').read_content())
    return url


@pytest.fixture
def courserecords_mock():
    url = 'https://www.parkrun.ru/results/courserecords/'
    responses.add(responses.GET, url, body=ParkrunMock('courserecords').read_content())
    return url


@responses.activate
def test_get_participants(monkeypatch):
    monkeypatch.setattr(parkrun, 'get_html_tree', ParkrunMock('consolidatedclub').get_html_tree)
    mes = parkrun.get_participants()
    assert 'Паркраны, где побывали наши одноклубники' in mes
    assert 'Kuzminki' in mes
    participants_count = [int(p) for p in re.findall(r'\((\d+)\xa0чел\.\)', mes, re.M)]
    participants_sum = int(re.search(r'Участвовало (\d+) из \d+ чел.', mes)[1])
    assert sum(participants_count) == participants_sum


def test_add_relevance_notification():
    message = parkrun.add_relevance_notification(date(2020, 1, 1))
    assert 'Извините' in message
    message = parkrun.add_relevance_notification(date.today().replace(month=date.today().month + 1))
    assert message == ''


@responses.activate
def test_get_club_table(clubhistory_mock):
    data = parkrun.get_club_table()
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock
    assert isinstance(data, pandas.DataFrame)
    assert not data.empty


@responses.activate
def test_get_kuzminki_fans(clubhistory_mock):
    message = parkrun.get_kuzminki_fans()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock


@responses.activate
def test_get_wr_parkruners(clubhistory_mock):
    message = parkrun.get_wr_parkruners()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock


@responses.activate
def test_get_kuzminki_top_results(clubhistory_mock):
    message = parkrun.get_kuzminki_top_results()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock


@responses.activate
def test_most_slow_parkruns(courserecords_mock):
    message = parkrun.most_slow_parkruns()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == courserecords_mock


def test_get_volunteers():
    message = parkrun.get_volunteers()
    print('\n', message)
    assert len(responses.calls) == 0
    assert '*Toп 10 волонтёров parkrun Kuzminki*' in message

# get_latest_results_diagram()
# make_latest_results_diagram('../utils/results.png', 'Титов').close()
# add_volunteers(204, 204)
# make_clubs_bar('../utils/clubs.png').close()
