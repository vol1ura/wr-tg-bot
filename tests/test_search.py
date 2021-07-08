import re

from utils.search import google, bashim


def test_google():
    message = google('бот, гречка')
    print(message)
    assert isinstance(message, str)
    assert not re.match(r'^бот', message, re.I)


def test_bashim():
    message = bashim('короновирус')
    print(message)
    assert isinstance(message, str)
