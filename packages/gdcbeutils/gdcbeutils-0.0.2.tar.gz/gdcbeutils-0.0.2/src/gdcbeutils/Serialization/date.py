"""
Support for date serialization
"""
from datetime import datetime


def define_start_end_of_day(date: datetime):
    tz_offset = date.tzinfo

    start_of_day = datetime(
        date.year,
        date.month,
        date.day,
        0,
        0,
        0,
        0,
        tzinfo=tz_offset,
    )

    end_of_day = datetime(
        date.year,
        date.month,
        date.day,
        23,
        59,
        59,
        9999,
        tzinfo=tz_offset,
    )

    return start_of_day, end_of_day
