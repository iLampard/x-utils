# -*- coding: utf-8 -*-


from collections import deque
from threading import Thread
from datetime import datetime as dt
import time
from xutils.date_utils import as_utc
from xutils.bar_builder.resamplebase import build_range
from xutils.bar_builder.bar_utils import build_bar
from xutils.bar_builder.bar import Bars


def utcnow():
    return as_utc(dt.utcnow())


class MarketSeries(object):
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

    def append(self, data_row):
        self.price_series.append(data_row[0])
        self.volume_series.append(data_row[1])
        self.amount_series.append(data_row[2])
        self.datetime_series.append(data_row[3])

    def is_empty(self):
        return len(self.price_series) == 0


class PollingThread(Thread):
    def __init__(self, tickers, live_quote_arg_func, inquery_period=3):
        super(PollingThread, self).__init__()
        self.tickers = tickers
        self.ticker_dict = {}
        self.last_quote_time = {}
        self.live_quote_arg_func = live_quote_arg_func
        self.inquery_period = inquery_period

        for ticker in tickers:
            self.ticker_dict[ticker] = MarketSeries()
            self.last_quote_time[ticker] = None

        self._stopped = False

    def _wait(self):
        for ticker in self.tickers:
            self.ticker_dict[ticker].reset()

        next_call = self.get_next_call_date_time()

        while not self._stopped and utcnow() < next_call:
            start_time = dt.now()
            self.load_data()
            end_time = dt.now()

            time_diff = (end_time - start_time).seconds

            if time_diff < self.inquery_period:
                time.sleep(self.inquery_period - time_diff)

    def load_data(self):
        try:
            df = self.live_quote_arg_func(self.tickers)
            for index, ticker in enumerate(self.tickers):
                ticker_info = df.loc[index]
                self.ticker_dict[ticker].append(ticker_info)
        except Exception:
            raise ValueError('Polling thread exception')

    def get_next_call_date_time(self):
        raise NotImplementedError

    def do_call(self):
        raise NotImplementedError

    def run(self):
        while not self._stopped:
            self._wait()
            if not self._stopped:
                self.do_call()

    def _update_next_bar_close(self):
        raise NotImplementedError

    def stop(self):
        self._stopped = True

    def stopped(self):
        return self._stopped


class BarThread(PollingThread):
    def __init__(self, tickers, inquery_period, frequency, queue, live_quote_arg_func, **kwargs):
        super(BarThread, self).__init__(tickers, live_quote_arg_func, inquery_period)
        self.queue = queue
        self.frequency = frequency
        self.next_bar_close = None
        self.on_bar_event = kwargs.get('on_bar_event', 1)
        self._update_next_bar_close()

    def _update_next_bar_close(self):
        self.next_bar_close = build_range(utcnow(), self.frequency).ending

    def get_next_call_date_time(self):
        return self.next_bar_close

    def do_call(self):
        end_time = self.next_bar_close
        self._update_next_bar_close()
        bar_dict = {}

        for ticker in self.tickers:
            if not self.ticker_dict[ticker].is_empty():
                bar_dict[ticker] = build_bar(end_time, self.ticker_dict[ticker])

        if len(bar_dict):
            bars = Bars(bar_dict)
            self.queue.put((self.on_bar_event, bars))
