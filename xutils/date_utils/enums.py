# -*- coding: utf-8 -*-

from enum import IntEnum
from enum import unique


@unique
class TimeUnits(IntEnum):
    BDays = 0
    Days = 1
    Weeks = 2
    Months = 3
    Years = 4


@unique
class NormalizingType(IntEnum):
    Null = 0
    BizDay = 1
    CalendarDay = 2


@unique
class DateGeneration(IntEnum):
    Zero = 0
    Backward = 1
    Forward = 2


@unique
class BizDayConventions(IntEnum):
    Following = 0
    ModifiedFollowing = 1
    Preceding = 2
    ModifiedPreceding = 3
    Unadjusted = 4
    HalfMonthModifiedFollowing = 5
    Nearest = 6


@unique
class Months(IntEnum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


@unique
class Weekdays(IntEnum):
    Sunday = 1
    Monday = 2
    Tuesday = 3
    Wednesday = 4
    Thursday = 5
    Friday = 6
    Saturday = 7
