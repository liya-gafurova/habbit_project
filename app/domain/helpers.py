from enum import IntEnum

"""
PeriodN (object Value - from Architecture Patterns with Python): 
    - days of the week 
    - time 

1 unit of Period - 1 week
1 unit of Doc - 1 month
1 unit of Habit - 1 Period
"""


class DaysOfWeek(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Months(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12
