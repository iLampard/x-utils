# -*- coding: utf-8 -*-

# ref: https://github.com/Yam-cn/pyalgotrade-cn/blob/master/pyalgotrade/cn/bar.py


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
    # Optimization to reduce memory footprint.
    __slots__ = (
        'trade_date',
        'open',
        'close',
        'high',
        'low',
        'volume',
        'amount',
        'frequency',
        'extra',
    )

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
        self.open = open_
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.amount = amount
        self.frequency = frequency
        self.extra = extra

    def __setstate__(self, state):
        (self.trade_date,
         self.open,
         self.close,
         self.high,
         self.low,
         self.volume,
         self.amount,
         self.frequency,
         self.extra) = state

    def __getstate__(self):
        return (
            self.trade_date,
            self.open,
            self.close,
            self.high,
            self.low,
            self.volume,
            self.amount,
            self.frequency,
            self.extra
        )

    @property
    def datetime(self):
        return self.trade_date

    @property
    def freq(self):
        return self.frequency

    @property
    def price(self):
        return self.close

    @property
    def extra_columns(self):
        return self.extra


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
        for instrument, current_bar in bar_dict.iteritems():
            if first_trade_date is None:
                first_trade_date = current_bar.datetime
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
    def datetime(self):
        """Returns the :class:`datetime.datetime` for this set of bars."""
        return self.trade_date

    def get_bar(self, instrument):
        """Returns the :class:`BasicBar` for the given instrument or None if the instrument is not found."""
        return self.bar_dict.get(instrument, None)

