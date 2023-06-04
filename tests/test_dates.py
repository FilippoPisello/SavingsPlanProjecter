import datetime
import random

import pytest

from savings_plan_projecter.days import Day, date_range


def test_if_number_of_days_is_negative_then_error():
    start_date = datetime.date(2023, 1, 1)
    with pytest.raises(ValueError):
        date_range(start_date, number_of_days=-1)


def test_if_number_of_days_is_valid_then_date_range():
    start_date = datetime.date(2023, 1, 1)

    actual = date_range(start_date, 3)
    expected = [
        Day.from_date(start_date),
        Day.from_date(datetime.date(2023, 1, 2)),
        Day.from_date(datetime.date(2023, 1, 3)),
    ]
    assert actual == expected


def test_first_working_day_in_month_is_one_and_only_one():
    for _ in range(100):
        month = random.randint(1, 12)
        year = random.randint(1, 3000)
        start_date = datetime.date(year, month, 1)
        dates = date_range(start_date, 15)

        day_first_working_day = [
            day for day in dates if day.is_first_working_day_of_month
        ]
        assert len(day_first_working_day) == 1
