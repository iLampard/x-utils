# -*- coding: utf-8 -*-

from __future__ import division
import re
from math import floor
from copy import deepcopy
from xutils.date_utils.enums import TimeUnits
from xutils.assert_utils import py_assert

_unitPattern = re.compile('[BbDdMmWwYy]{1}')
_numberPattern = re.compile('[-+]*[0-9]+')

_unitsDict = {'d': TimeUnits.Days,
              'b': TimeUnits.BDays,
              'w': TimeUnits.Weeks,
              'm': TimeUnits.Months,
              'y': TimeUnits.Years}


class Period(object):
    def __init__(self, reprStr=None, length=0, units=0):

        if reprStr:
            unitsPos = _unitPattern.search(reprStr)
            numPos = _numberPattern.search(reprStr)
            unitsStr = reprStr[unitsPos.start():unitsPos.end()].lower()
            n = int(reprStr[numPos.start():numPos.end()])
            self._length = n
            self._units = int(_unitsDict[unitsStr])
        else:
            self._length = length
            self._units = units

    @property
    def length(self):
        return self._length

    @property
    def units(self):
        return self._units

    def normalize(self):
        length = self.length
        units = self.units
        if self.length != 0:
            if units == TimeUnits.BDays or units == TimeUnits.Weeks or units == TimeUnits.Years:
                return Period(length=length, units=units)
            elif units == TimeUnits.Months:
                if length % 12 == 0:
                    length //= 12
                    units = TimeUnits.Years
                return Period(length=length, units=units)
            elif units == TimeUnits.Days:
                if length % 7 == 0:
                    length //= 7
                    units = TimeUnits.Weeks
                return Period(length=length, units=units)
            else:
                raise TypeError("wrong period units type {0}".format(self.units))

    def __div__(self, n):
        resunits = self.units
        reslength = self.length

        if reslength % n == 0:
            reslength /= n
        else:
            if resunits == TimeUnits.Years:
                reslength *= 12
                resunits = TimeUnits.Months
            elif resunits == TimeUnits.Weeks:
                reslength *= 7
                resunits = TimeUnits.Days

            py_assert(reslength % n == 0, ValueError, "{0} cannot be divided by {1:d}".format(self, n))

            reslength //= n

        return Period(length=reslength, units=resunits)

    # only work for python 3
    def __truediv__(self, n):
        return self.__div__(n)

    def __add__(self, p2):
        reslength = self.length
        resunits = self.units
        p2length = p2.length
        p2units = p2.units

        if reslength == 0:
            return Period(length=p2length, units=p2units)
        elif resunits == p2units:
            reslength += p2length
            return Period(length=reslength, units=resunits)
        else:
            if resunits == TimeUnits.Years:
                if p2units == TimeUnits.Months:
                    resunits = TimeUnits.Months
                    reslength = reslength * 12 + p2length
                elif p2units == TimeUnits.Weeks or p2units == TimeUnits.Days or p2units == TimeUnits.BDays:
                    py_assert(p2length == 0, ValueError, "impossible addition between {0} and {1}".format(self, p2))
                else:
                    raise ValueError("unknown time unit ({0:d})".format(p2units))
                return Period(length=reslength, units=resunits)
            elif resunits == TimeUnits.Months:
                if p2units == TimeUnits.Years:
                    reslength += 12 * p2length
                elif p2units == TimeUnits.Weeks or p2units == TimeUnits.Days or p2units == TimeUnits.BDays:
                    py_assert(p2length == 0, ValueError, "impossible addition between {0} and {1}".format(self, p2))
                else:
                    raise ValueError("unknown time unit ({0:d})".format(p2units))
                return Period(length=reslength, units=resunits)
            elif resunits == TimeUnits.Weeks:
                if p2units == TimeUnits.Days:
                    resunits = TimeUnits.Days
                    reslength = reslength * 7 + p2length
                elif p2units == TimeUnits.Years or p2units == TimeUnits.Months or p2units == TimeUnits.BDays:
                    py_assert(p2length == 0, ValueError, "impossible addition between {0} and {1}".format(self, p2))
                else:
                    raise ValueError("unknown time unit ({0:d})".format(p2units))
                return Period(length=reslength, units=resunits)
            elif resunits == TimeUnits.Days:
                if p2units == TimeUnits.Weeks:
                    reslength += 7 * p2length
                elif p2units == TimeUnits.Years or p2units == TimeUnits.Months or p2units == TimeUnits.BDays:
                    py_assert(p2length == 0, ValueError, "impossible addition between {0} and {1}".format(self, p2))
                else:
                    raise ValueError("unknown time unit ({0:d})".format(p2units))
                return Period(length=reslength, units=resunits)
            elif resunits == TimeUnits.BDays:
                if p2units == TimeUnits.Years or p2units == TimeUnits.Months or p2units == TimeUnits.Weeks or p2units == TimeUnits.Days:
                    py_assert(p2length == 0, ValueError, "impossible addition between {0} and {1}".format(self, p2))
                else:
                    raise ValueError("unknown time unit ({0:d})".format(p2units))
                return Period(length=reslength, units=resunits)

    def __neg__(self):
        return Period(length=-self.length, units=self.units)

    def __sub__(self, p2):
        return self + (-p2)

    def __lt__(self, p2):

        if self.length == 0:
            return p2.length > 0

        if p2.length == 0:
            return self.length < 0

        # exact comparisons
        if self.units == p2.units:
            return self.length < p2.length
        elif self.units == TimeUnits.Months and p2.units == TimeUnits.Years:
            return self.length < (p2.length * 12)
        elif self.units == TimeUnits.Years and p2.units == TimeUnits.Months:
            return (self.length * 12) < p2.length
        elif self.units == TimeUnits.Days and p2.units == TimeUnits.Weeks:
            return self.length < (p2.length * 7)
        elif self.units == TimeUnits.Weeks and p2.units == TimeUnits.Days:
            return (self.length * 7) < p2.length

        # inexact comparisons (handled by converting to days and using limits)

        p1lim = _days_min_max(self)
        p2lim = _days_min_max(p2)

        if p1lim[1] < p2lim[0]:
            return True
        elif p1lim[0] >= p2lim[1]:
            return False
        else:
            raise ValueError("undecidable comparison between {0} and {1}".format(self, p2))

    def __eq__(self, p2):
        return not (self < p2 or p2 < self)

    def __ne__(self, p2):
        return not self == p2

    def __gt__(self, p2):
        return p2 < self

    def __str__(self):
        out = ""
        n = self.length
        m = 0
        units = self.units

        if units == TimeUnits.Days:
            if n >= 7:
                m = int(floor(n / 7, ))
                out = '{0}W'.format(m)
                n %= 7
            if n != 0 or m == 0:
                return '{0}{1}D'.format(out, n)
            else:
                return out
        elif units == TimeUnits.Weeks:
            return '{0}W'.format(n)
        elif units == TimeUnits.Months:
            if n >= 12:
                m = int(floor(n / 12.))
                out = '{0}Y'.format(m)
                n %= 12
            if n != 0 or m == 0:
                return '{0}{1}M'.format(out, n)
            else:
                return out
        elif units == TimeUnits.Years:
            return '{0}Y'.format(n)
        elif units == TimeUnits.BDays:
            return '{0}B'.format(n)

    def __deepcopy__(self, memo):
        return Period(length=self.length, units=self.units)

    def __reduce__(self):
        d = {}

        return Period, (None, self.length, self.units), d

    def __setstate__(self, state):
        pass


def check_period(p):
    return p if isinstance(p, Period) else Period(p)


def _days_min_max(p):
    units = p.units
    length = p.length
    if units == TimeUnits.Days:
        return length, length
    elif units == TimeUnits.Weeks:
        return 7 * length, 7 * length
    elif units == TimeUnits.Months:
        return 28 * length, 31 * length
    elif units == TimeUnits.Years:
        return 365 * length, 366 * length
    elif units == TimeUnits.BDays:
        raise ValueError("Business days unit has not min max days")
