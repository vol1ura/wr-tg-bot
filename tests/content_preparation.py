import requests

from utils.parkrun import parkrun_headers


def prepare_club_participants():
    result = requests.get('https://www.parkrun.com/results/consolidatedclub/?clubNum=23212', headers=parkrun_headers)
    with open('content/consolidatedclub.html', 'w') as f:
        f.write(result.text)


def prepare_club_records():
    result = requests.get('https://www.parkrun.ru/kuzminki/results/clubhistory/?clubNum=23212', headers=parkrun_headers)
    with open('content/clubhistory.html', 'w') as f:
        f.write(result.text)


def prepare_courserecords():
    result = requests.get('https://www.parkrun.ru/results/courserecords/', headers=parkrun_headers)
    with open('content/courserecords.html', 'w') as f:
        f.write(result.text)


if __name__ == '__main__':
    # prepare_club_participants()
    # prepare_club_records()
    prepare_courserecords()
