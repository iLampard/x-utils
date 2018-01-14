# -*- coding: utf-8 -*-


from collections import deque
from threading import Thread


class TickDataSeries(object):
    def __init__(self):
        self.price_series = deque()
        self.volume_series = deque()
        self.amount_series = deque()
        self.datetime_series = deque()

    def reset(self):
        self.price_series.clear()
        self.volume_series.clear()
        self.amount_series.clear()
        self.datetime_series = deque()

    @property
    def price(self):
        return self.price_series

    @property
    def volume(self):
        return self.volume_series

    @property
    def amount(self):
        return self.amount_series

    @property
    def date_time(self):
        return self.datetime_series

    def append(self, price, volume, amount, date_time):
        self.price_series.append(price)
        self.volume_series.append(volume)
        self.amount_series.append(amount)
        self.datetime_series.append(date_time)

    def is_empty(self):
        return len(self.price_series) == 0


class PollingThread(Thread):
    def __init__(self, tickers, inquery_period=3):
        super(PollingThread, self).__init__()
        self.tickers = tickers
        self.tick_dict = {}
        self.last_quote_time = {}
        self.inquery_period = inquery_period

        for ticker in tickers:
            self.tick_dict[ticker] = TickDataSeries()
            self.last_quote_time[ticker] = None

        self._stopped = False

    def _wait(self):
        for ticker in self.tickers:
            self.tick_dict[ticker].reset()

    def get_next_call_date_time(self):
        raise NotImplementedError

    def do_call(self):
        raise NotImplementedError

    def run(self):
        while not self._stopped:
            self._wait()
            if not self._stopped:
                self.do_call()






