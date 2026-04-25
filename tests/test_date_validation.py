import datetime

from utils import date_validator


def test_check_in_date_is_valid_for_today():
    today = datetime.date.today()
    assert date_validator.check_in_date_is_valid(today.year, today.month, today.day) is True


def test_check_in_date_is_invalid_for_yesterday():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    assert date_validator.check_in_date_is_valid(yesterday.year, yesterday.month, yesterday.day) is False


def test_check_out_date_is_valid_when_equal_to_check_in():
    assert date_validator.check_out_date_is_valid(2026, 4, 20, 2026, 4, 20) is True


def test_check_out_date_is_invalid_when_earlier():
    assert date_validator.check_out_date_is_valid(2026, 4, 20, 2026, 4, 19) is False


def test_check_out_date_is_invalid_when_date_does_not_exist():
    assert date_validator.check_out_date_is_valid(2026, 4, 20, 2026, 2, 31) is False
