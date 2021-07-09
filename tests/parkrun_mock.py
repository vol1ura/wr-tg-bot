import os
import time

import requests
from lxml.html import fromstring

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
