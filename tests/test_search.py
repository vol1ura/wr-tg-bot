import re

import responses

from utils.search import google, bashim


def test_google():
    message = google('бот, гречка')
    print(message)
    assert isinstance(message, str)
    assert not re.match(r'^бот', message, re.I)


@responses.activate
def test_google_fail():
    search_url = 'https://www.googleapis.com/customsearch/v1?'
    responses.add(responses.GET, re.compile(search_url + '.*'), json={'items': 'wrong json'})
    message = google('test')
    assert len(responses.calls) == 1
    assert message == ''
    assert responses.calls[0].request.url.startswith(search_url)


def test_bashim():
    message = bashim('короновирус')
    print(message)
    assert isinstance(message, str)
