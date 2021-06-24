import re
from datetime import date

from utils.news import get_competitions, club_calendar


def test_get_competitions():
    date_today = date.today()
    competitions = get_competitions(date_today.month, date_today.year)
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
