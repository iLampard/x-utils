# -*- coding: utf-8 -*-


import abc
import six
import datetime as dt
from argcheck import *
from xutils.bar_builder.bar import BarFrequency


@six.add_metaclass(abc.ABCMeta)
class TimeRange(object):
    @abc.abstractmethod
    def belongs(self, date_time):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_begin(self):
        raise NotImplementedError()

    # 1 past the end
    @abc.abstractmethod
    def get_end(self):
        raise NotImplementedError()


class IntraDayRange(TimeRange):
    @expect_types(frequency=int)
    @expect_bounded(frequency=(1, BarFrequency.DAY))
    def __init__(self, date_time, frequency):
        super(IntraDayRange, self).__init__()
        ts = int(dt.datetime_to_timestamp(date_time))
        slot = int(ts / frequency)
        slotTs = slot * frequency
        self.begin = dt.timestamp_to_datetime(slotTs, not dt.datetime_is_naive(date_time))
        if not dt.datetime_is_naive(date_time):
            self.begin = dt.localize(self.__begin, date_time.tzinfo)
        self.end = self.begin + date_time.timedelta(seconds=frequency)
