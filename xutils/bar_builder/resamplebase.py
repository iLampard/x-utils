# -*- coding: utf-8 -*-


import abc
import six
from argcheck import *
from datetime import timedelta
from datetime import datetime as dt
from xutils.bar_builder.bar import BarFrequency
from xutils.date_utils import DatetimeConverter
from xutils.date_utils import (localize,
                               datetime_is_naive)


@six.add_metaclass(abc.ABCMeta)
class TimeRange(object):
    @abc.abstractmethod
    def belongs(self, date_time):
        raise NotImplementedError()

    @abc.abstractmethod
    def beginning(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def ending(self):
        raise NotImplementedError()


class IntraDayRange(TimeRange):
    @expect_types(frequency=int)
    @expect_bounded(frequency=(1, BarFrequency.DAY))
    def __init__(self, date_time, frequency):
        super(IntraDayRange, self).__init__()
        ts = int(DatetimeConverter.datetime_to_timestamp(date_time))
        slot = int(ts / frequency)
        slot_ts = slot * frequency
        self.begin = DatetimeConverter.timestamp_to_datetime(slot_ts, not datetime_is_naive(date_time))
        if not datetime_is_naive(date_time):
            self.begin = localize(self.__begin, date_time.tzinfo)
        self.end = self.begin + date_time.timedelta(seconds=frequency)

    def belongs(self, date_time):
        return self.end > date_time >= self.begin

    @property
    def beginning(self):
        return self.begin

    @property
    def ending(self):
        return self.end


class DayRange(TimeRange):
    def __init__(self, date_time):
        super(DayRange, self).__init__()
        self.begin = dt(date_time.year, date_time.month, date_time.day)
        if not datetime_is_naive(date_time):
            self.begin = localize(date_time, date_time.tzinfo)
        self.end = self.begin + timedelta(days=1)

    def belongs(self, date_time):
        return self.end > date_time >= self.begin

    @property
    def beginning(self):
        return self.begin

    @property
    def ending(self):
        return self.end


@expect_types(date_time=dt)
def build_range(date_time, frequency):
    if frequency < BarFrequency.DAY:
        return IntraDayRange(date_time, frequency)
    elif frequency == BarFrequency.DAY:
        return DayRange(date_time)
    else:
        raise NotImplementedError
