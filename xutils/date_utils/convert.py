# -*- coding: utf-8 -*-

import datetime
import pytz


# ref: https://github.com/Yam-cn/pyalgotrade-cn/blob/master/pyalgotrade/utils/dt.py


def datetime_is_naive(date_time):
    """ Returns True if dateTime is naive."""
    return date_time.tzinfo is None or date_time.tzinfo.utcoffset(date_time) is None


def localize(date_time, time_zone):
    """Returns a datetime adjusted to a timezone:
     * If dateTime is a naive datetime (datetime with no timezone information), timezone information is added but date
       and time remains the same.
     * If dateTime is not a naive datetime, a datetime object with new tzinfo attribute is returned, adjusting the date
       and time data so the result is the same UTC time.
    """

    if datetime_is_naive(date_time):
        ret = time_zone.localize(date_time)
    else:
        ret = date_time.astimezone(time_zone)
    return ret


def as_utc(date_time):
    return localize(date_time, pytz.utc)


class DatetimeConverter(object):
    def __init__(self):
        pass

    @classmethod
    def datetime_to_timestamp(cls, date_time):
        """ Converts a datetime.datetime to a UTC timestamp."""
        diff = as_utc(date_time) - epoch_utc
        return diff.total_seconds()

    @classmethod
    def timestamp_to_datetime(cls, time_stamp, localized=True):
        """ Converts a UTC timestamp to a datetime.datetime."""
        ret = datetime.datetime.utcfromtimestamp(time_stamp)
        if localized:
            ret = localize(ret, pytz.utc)
        return ret


epoch_utc = as_utc(datetime.datetime(1970, 1, 1))
