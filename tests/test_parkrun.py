import os
import re
import time
from datetime import date

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
        'courserecords': 'https://www.parkrun.ru/results/courserecords/',
        'latestresults': 'https://www.parkrun.ru/kuzminki/results/latestresults/'
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
        time.sleep(2.03)
        result = requests.get(ParkrunMock.PARKRUN_PAGES[self.__page], headers=parkrun_headers)
        with open(self.__page_path, 'w') as f:
            f.write(result.text)


@pytest.fixture(scope='session', autouse=True)
def prepare_parkrun_pages():
    for page_name in ParkrunMock.PARKRUN_PAGES.keys():
        ParkrunMock(page_name)


@pytest.fixture(autouse=True)
def parkrun_mock():
    for page_name, page_url in ParkrunMock.PARKRUN_PAGES.items():
        parkrun_page = ParkrunMock(page_name)
        responses.add(responses.GET, page_url, body=parkrun_page.read_content())


def test_get_participants(monkeypatch):
    monkeypatch.setattr(parkrun, 'get_html_tree', ParkrunMock('consolidatedclub').get_html_tree)
    mes = parkrun.get_participants()
    assert 'Паркраны, где побывали наши одноклубники' in mes
    assert 'https://www.parkrun.ru/' in mes
    participants_count = [int(p) for p in re.findall(r'\((\d+)\xa0чел\.\)', mes, re.M)]
    participants_sum = int(re.search(r'Участвовало (\d+) из \d+ чел.', mes)[1])
    assert sum(participants_count) == participants_sum


def test_add_relevance_notification():
    message = parkrun.add_relevance_notification(date(2020, 1, 1))
    assert 'Извините' in message
    message = parkrun.add_relevance_notification(date.today().replace(month=date.today().month + 1))
    assert message == ''


@responses.activate
def test_get_club_table():
    data = parkrun.get_club_table()
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()
    assert isinstance(data, pandas.DataFrame)
    assert not data.empty


@responses.activate
def test_get_kuzminki_fans():
    message = parkrun.get_kuzminki_fans()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


@responses.activate
def test_get_wr_parkruners():
    message = parkrun.get_wr_parkruners()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


@responses.activate
def test_get_kuzminki_top_results():
    message = parkrun.get_kuzminki_top_results()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


@responses.activate
def test_most_slow_parkruns():
    message = parkrun.most_slow_parkruns()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


def test_get_volunteers():
    message = parkrun.get_volunteers()
    print('\n', message)
    assert len(responses.calls) == 0
    assert '*Toп 10 волонтёров parkrun Kuzminki*' in message


@responses.activate
def test_make_latest_results_diagram(tmpdir):
    pic_path = tmpdir.join('results.png')
    start_time = time.time()
    parkrun.make_latest_results_diagram(pic_path).close()
    assert time.time() < start_time + 4
    assert os.path.exists(pic_path)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


@responses.activate
def test_make_clubs_bar(tmpdir):
    pic_path = tmpdir.join('club.png')
    start_time = time.time()
    parkrun.make_clubs_bar(pic_path).close()
    assert time.time() < start_time + 4
    assert os.path.exists(pic_path)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()
