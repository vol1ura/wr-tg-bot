import os
import re
import time
from datetime import date

import pandas
import pytest
import responses
from numpy.random import randint

from tests.parkrun_mock import ParkrunMock
from utils import parkrun


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
def test_get_latest_results_df():
    df, number_runners, parkrun_date = parkrun.get_latest_results_df()
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()
    assert isinstance(df, pandas.DataFrame)
    assert isinstance(number_runners, int)
    assert number_runners > 0
    assert isinstance(parkrun_date, str)
    dd, mm, yyyy = parkrun_date.split('/')
    assert 0 < int(dd) <= 31
    assert 0 < int(mm) <= 12
    assert int(yyyy) >= date.today().year - 1


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


@pytest.mark.parametrize('t, phi', zip(randint(900, size=10), randint(3 * 360, size=10)))
@responses.activate
def test_make_latest_results_diagram_personal(tmpdir, t, phi):
    df = parkrun.get_latest_results_df()[0].reset_index(drop=True)
    athlete_name = re.search(r'([А-ЯЁ ]+)\d', df.iloc[t % len(df), 1])[1].strip()
    if not athlete_name:
        return
    print(athlete_name)
    pic_path = tmpdir.join('results.png')
    start_time = time.time()
    parkrun.make_latest_results_diagram(pic_path, athlete_name, phi).close()
    assert time.time() < start_time + 4
    assert os.path.exists(pic_path)
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


@responses.activate
def test_make_latest_results_diagram_personal_exception(tmpdir):
    pic_path = tmpdir.join('results.png')
    start_time = time.time()
    with pytest.raises(AttributeError):
        parkrun.make_latest_results_diagram(pic_path, 'wrong_athlete_name').close()
    assert time.time() < start_time + 4
    assert not os.path.exists(pic_path)
    assert responses.calls[0].request.url in ParkrunMock.PARKRUN_PAGES.values()


def test_add_volunteers(monkeypatch, tmpdir):
    volunteers_file = tmpdir.join('kuzminki_full_stat.txt')
    monkeypatch.setattr(parkrun, 'VOLUNTEERS_FILE', volunteers_file)
    parkrun.add_volunteers(2, 3)
    assert os.path.exists(volunteers_file)
    with open(volunteers_file) as f:
        volunteers_info = f.readlines()
    for line in volunteers_info:
        assert re.fullmatch('kuzminki\t[23]\tA\\d+( \\w+){2,}', line.rstrip())
    print(volunteers_info)
