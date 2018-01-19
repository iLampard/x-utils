# -*- coding: utf-8 -*-

# ref: https://github.com/Yam-cn/pyalgotrade-cn/blob/master/pyalgotrade/cn/bar.py

import six

class BarFrequency(object):
    """Enum like class for bar frequencies. Valid values are:
    * **Frequency.TRADE**: The bar represents a single trade.
    * **Frequency.SECOND**: The bar summarizes the trading activity during 1 second.
    * **Frequency.MINUTE**: The bar summarizes the trading activity during 1 minute.
    * **Frequency.HOUR**: The bar summarizes the trading activity during 1 hour.
    * **Frequency.DAY**: The bar summarizes the trading activity during 1 day.
    * **Frequency.WEEK**: The bar summarizes the trading activity during 1 week.
    * **Frequency.MONTH**: The bar summarizes the trading activity during 1 month.
    """

    # It is important for frequency values to get bigger for bigger windows.
    TRADE = -1
    SECOND = 1
    MINUTE = 60
    HOUR = 60 * 60
    DAY = 24 * 60 * 60
    WEEK = 24 * 60 * 60 * 7
    MONTH = 24 * 60 * 60 * 31


class BasicBar(object):
    def __init__(self, trade_date, open_, high, low, close, volume, amount, frequency, extra={}):
        if high < low:
            raise Exception("high < low on %s" % trade_date)
        elif high < open_:
            raise Exception("high < open on %s" % trade_date)
        elif high < close:
            raise Exception("high < close on %s" % trade_date)
        elif low > open_:
            raise Exception("low > open on %s" % trade_date)
        elif low > close:
            raise Exception("low > close on %s" % trade_date)

        self.trade_date = trade_date
        self._open = open_
        self._close = close
        self._high = high
        self._low = low
        self._volume = volume
        self._amount = amount
        self._frequency = frequency
        self._extra = extra

    def __setstate__(self, state):
        (self.trade_date,
         self._open,
         self._close,
         self._high,
         self._low,
         self._volume,
         self._amount,
         self._frequency,
         self._extra) = state

    def __getstate__(self):
        return (
            self.trade_date,
            self._open,
            self._close,
            self._high,
            self._low,
            self._volume,
            self._amount,
            self._frequency,
            self._extra
        )

    @property
    def date_time(self):
        return self.trade_date

    @property
    def freq(self):
        return self._frequency

    @property
    def price(self):
        return self._close

    @property
    def open(self):
        return self._open

    @property
    def high(self):
        return self._high

    @property
    def low(self):
        return self._low

    @property
    def close(self):
        return self._close

    @property
    def volume(self):
        return self._volume

    @property
    def extra_columns(self):
        return self._extra


class Bars(object):
    """A group of :class:`Bar` objects.
    :param bar_dict: A map of instrument to :class:`BasicBar` objects.
    :type bar_dict: map.
    .. note::
        All bars must have the same datetime.
    """

    def __init__(self, bar_dict):
        if len(bar_dict) == 0:
            raise Exception("No bars supplied")

        # Check that bar datetimes are in sync
        first_trade_date = None
        first_instrument = None
        for instrument, current_bar in six.iteritems(bar_dict):
            if first_trade_date is None:
                first_trade_date = current_bar.date_time
                first_instrument = instrument
            elif current_bar.datetime != first_trade_date:
                raise Exception("Bar data times are not in sync. %s %s != %s %s" % (
                    instrument,
                    current_bar.datetime,
                    first_instrument,
                    first_trade_date
                ))

        self.bar_dict = bar_dict
        self.trade_date = first_trade_date

    def __getitem__(self, instrument):
        """Returns the :class:`Basicbar` for the given instrument.
        If the instrument is not found an exception is raised."""
        return self.bar_dict[instrument]

    def __contains__(self, instrument):
        """Returns True if a :class:`Basicbar` for the given instrument is available."""
        return instrument in self.bar_dict

    @property
    def items(self):
        return self.bar_dict.items()

    @property
    def keys(self):
        return self.bar_dict.keys()

    @property
    def instruments(self):
        """Returns the instrument symbols."""
        return self.bar_dict.keys()

    @property
    def date_time(self):
        """Returns the :class:`datetime.datetime` for this set of bars."""
        return self.trade_date

    def get_bar(self, instrument):
        """Returns the :class:`BasicBar` for the given instrument or None if the instrument is not found."""
        return self.bar_dict.get(instrument, None)
