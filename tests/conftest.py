import os

import pytest
from dotenv import load_dotenv

from tests.parkrun_mock import ParkrunMock


@pytest.fixture(scope='session', autouse=True)
def test_dot_env_mock():
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


@pytest.fixture(scope='session', autouse=True)
def prepare_parkrun_pages():
    for page_name in ParkrunMock.PARKRUN_PAGES.keys():
        ParkrunMock(page_name)
