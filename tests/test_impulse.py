import datetime
from utils.impulse import ImpulseChallenge


def test_get_payload():
    today = datetime.date(2022, 1, 11)
    payload = ImpulseChallenge()._ImpulseChallenge__get_payload(today)
    assert payload['func'] == 'get_Clubs_Year'
    assert payload['json_v'][0]['arg']['Week'] == '02'
    assert payload['json_v'][0]['arg']['Year'] == '2022'


def test_make_mark():
    mark_short = ImpulseChallenge()._ImpulseChallenge__make_mark('Test Name')
    assert 'Test Name' == mark_short
    mark_long = ImpulseChallenge()._ImpulseChallenge__make_mark('Test1Name abcd_+:;z23')
    assert 'Test1Name abcd_+:;...' == mark_long
