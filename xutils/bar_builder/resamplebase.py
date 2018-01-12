# -*- coding: utf-8 -*-


import abc
import six
from argcheck import *
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
        ts = int(DatetimeConverter.datetime_to_timestamp(date_time))
        slot = int(ts / frequency)
        slot_ts = slot * frequency
        self.begin = DatetimeConverter.timestamp_to_datetime(slot_ts, not datetime_is_naive(date_time))
        if not datetime_is_naive(date_time):
            self.begin = localize(self.__begin, date_time.tzinfo)
        self.end = self.begin + date_time.timedelta(seconds=frequency)
