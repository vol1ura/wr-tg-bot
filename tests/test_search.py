import os
import re

from dotenv import load_dotenv

from utils.search import google, bashim

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def test_google():
    message = google('бот, гречка')
    print(message)
    assert isinstance(message, str)
    assert not re.match(r'^бот', message, re.I)


def test_bashim():
    message = bashim('короновирус')
    print(message)
    assert isinstance(message, str)
