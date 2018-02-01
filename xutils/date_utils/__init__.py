# -*- coding: utf-8 -*-

from xutils.date_utils.date import Date
from xutils.date_utils.period import Period
from xutils.date_utils.calendar import Calendar
from xutils.date_utils.schedule import Schedule
from xutils.date_utils.misc import is_within_hour_range
from xutils.date_utils.enums import (TimeUnits,
                                     NormalizingType,
                                     DateGeneration,
                                     BizDayConventions,
                                     Months,
                                     Weekdays)
from xutils.date_utils.convert import (DatetimeConverter,
                                       datetime_is_naive,
                                       localize,
                                       as_utc)
import time

__all__ = ['Date',
           'Period',
           'Calendar',
           'Schedule',
           'is_within_hour_range',
           'TimeUnits',
           'NormalizingType',
           'DateGeneration',
           'BizDayConventions',
           'Months',
           'Weekdays',
           'DatetimeConverter',
           'datetime_is_naive',
           'localize',
           'as_utc',
           'is_tradetime_now']


def is_tradetime_now():
    """
    判断目前是不是交易时间, 并没有对节假日做处理
    :return: bool
    """
    now_time = time.localtime()
    now = (now_time.tm_hour, now_time.tm_min, now_time.tm_sec)
    if (9, 15, 0) <= now <= (11, 30, 0) or (13, 0, 0) <= now <= (15, 0, 0):
        return True
    return False
