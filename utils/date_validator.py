import datetime


def check_in_date_is_valid(year: int, month: int, day: int) -> bool:
    """
    Проверяет, что дата заезда не раньше сегодняшнего дня.
    """
    try:
        check_in = datetime.date(year=year, month=month, day=day)
    except ValueError:
        return False
    return check_in >= datetime.date.today()


def check_out_date_is_valid(
    check_in_year: int,
    check_in_month: int,
    check_in_day: int,
    check_out_year: int,
    check_out_month: int,
    check_out_day: int
) -> bool:
    """
    Проверяет, что дата выезда не раньше даты заезда.
    """
    try:
        check_in = datetime.date(year=check_in_year, month=check_in_month, day=check_in_day)
        check_out = datetime.date(year=check_out_year, month=check_out_month, day=check_out_day)
    except ValueError:
        return False
    return check_out >= check_in
