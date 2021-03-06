import re
from datetime import date, timedelta

import pytest

from utils.news import get_competitions, club_calendar


@pytest.mark.parametrize('test_date', [date.today() + timedelta(30 * d) for d in range(3)])
def test_get_competitions(test_date):
    competitions = get_competitions(test_date.month, test_date.year)
    print(competitions)
    assert isinstance(competitions, list)
    for competition in competitions:
        assert isinstance(competition, tuple)
        assert isinstance(competition[0], str)
        assert re.fullmatch(r'(\d\d - )?\d\d\.\d\d', competition[1])
        assert isinstance(competition[2], str)
        assert re.match(r'✏️<a href=\"http://probeg\.org/card\.php\?id=\d+\">.*</a>\n'
                        r'🕒.<b>Дата</b>: (\d\d - )?\d\d\.\d\d.| 📌.+ \(\w+\)', competition[2])


def test_club_calendar():
    message = club_calendar()
    assert re.fullmatch(
        r'Google-таблица 📅 стартов и участников 🏃\xa0Wake&Run:\n'
        r'<a href=\"https://docs\.google\.com/spreadsheets/d/\w+/edit\?usp=sharing\">📎\xa0Открыть</a>',
        message
    )
