import datetime
from dataclasses import dataclass
from typing import Self


@dataclass
class Day:
    year: int
    month: int
    day: int

    @property
    def date(self) -> datetime.date:
        return datetime.date(self.year, self.month, self.day)

    @property
    def weekday(self) -> int:
        return self.date.weekday()

    @property
    def is_working_day(self) -> bool:
        return self.weekday not in (5, 6)

    @property
    def is_first_working_day_of_month(self) -> bool:
        if not self.is_working_day:
            return False
        if self.day == 1:
            return True
        if self.day > 3:
            return False
        if self.weekday == 0:
            return True
        return False

    @classmethod
    def from_date(cls, date: datetime.date) -> Self:
        return cls(date.year, date.month, date.day)


def date_range(start: datetime.date, number_of_days: int) -> list[Day]:
    """Return a range of Day including start and the next n-1 days."""
    if number_of_days < 0:
        raise ValueError

    dates = []
    for i in range(number_of_days):
        dates.append(Day.from_date(start + datetime.timedelta(days=i)))

    return dates
