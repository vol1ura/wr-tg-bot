import os
import re

import pandas
import pytest
from lxml.html import fromstring

from utils import parkrun


class ParkrunMock:
    def __init__(self, page):
        self.__page_path = f'content/{page}.html'

    def read_content(self):
        page_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.__page_path)
        with open(page_path) as f:
            return f.read()

    def html_tree(self, _):
        return fromstring(self.read_content())


@pytest.fixture
def clubhistory_mock(responses):
    url = 'https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212'
    responses.add(responses.GET, url, body=ParkrunMock('clubhistory').read_content())
    return url


@pytest.fixture
def courserecords_mock(responses):
    url = 'https://www.parkrun.ru/results/courserecords/'
    responses.add(responses.GET, url, body=ParkrunMock('courserecords').read_content())
    return url


def test_get_participants(monkeypatch):
    monkeypatch.setattr(parkrun, 'get_html_tree', ParkrunMock('consolidatedclub').html_tree)
    mes = parkrun.get_participants()
    assert 'Паркраны, где побывали наши одноклубники' in mes
    assert 'Kuzminki' in mes
    participants_count = [int(p) for p in re.findall(r'\((\d+)\xa0чел\.\)', mes, re.M)]
    participants_sum = int(re.search(r'Участвовало (\d+) из \d+ чел.', mes)[1])
    assert sum(participants_count) == participants_sum


def test_get_club_table(responses, clubhistory_mock):
    data = parkrun.get_club_table()
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock
    assert isinstance(data, pandas.DataFrame)
    assert not data.empty


def test_get_kuzminki_fans(responses, clubhistory_mock):
    message = parkrun.get_kuzminki_fans()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock


def test_get_wr_parkruners(responses, clubhistory_mock):
    message = parkrun.get_wr_parkruners()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock


def test_get_kuzminki_top_results(responses, clubhistory_mock):
    message = parkrun.get_kuzminki_top_results()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == clubhistory_mock


def test_most_slow_parkruns(responses, courserecords_mock):
    message = parkrun.most_slow_parkruns()
    print('\n', message)
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == courserecords_mock

# get_latest_results_diagram()
# make_latest_results_diagram('../utils/results.png', 'Титов').close()
# add_volunteers(204, 204)
# make_clubs_bar('../utils/clubs.png').close()
