# -*- coding: utf-8 -*-


from collections import deque
from threading import Thread
from datetime import datetime as dt
import datetime
import time
import pytz
from xutils.date_utils import (localize,
                               as_utc)
from xutils.bar_builder.resamplebase import build_range
from xutils.bar_builder.bar_utils import build_bar
from xutils.bar_builder.bar import Bars


def utcnow():
    return as_utc(dt.utcnow())


def to_cn_market_time(date_time):
    time_zone = pytz.timezone('Asia/Shanghai')
    return localize(date_time, time_zone)


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

    def append(self, price, volume, amount, date_time):
        self.price_series.append(price)
        self.volume_series.append(volume)
        self.amount_series.append(amount)
        self.datetime_series.append(date_time)

    def is_empty(self):
        return len(self.price_series) == 0


class PollingThread(Thread):
    def __init__(self, tickers, inquery_period):
        super(PollingThread, self).__init__()
        self.tickers = tickers
        self.ticker_dict = {}
        self.inquery_period = inquery_period

        for ticker in tickers:
            self.ticker_dict[ticker] = MarketSeries()

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
        raise NotImplementedError

    def build_bar(self, date_time, ticker_info):
        raise NotImplementedError

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
        super(BarThread, self).__init__(tickers, inquery_period)
        self.queue = queue
        self.frequency = frequency
        self.next_bar_close = None
        self.live_quote_arg_func = live_quote_arg_func
        self.on_bar_event = kwargs.get('on_bar_event', 1)
        self._update_next_bar_close()

    def _update_next_bar_close(self):
        self.next_bar_close = build_range(utcnow(), self.frequency).ending

    # 检查是否为交易时间
    @staticmethod
    def _is_trade_time(dt_to_check):
        b = ((dt_to_check >= datetime.time(9, 30, 0)) & (dt_to_check <= datetime.time(11, 30, 0))) | \
            (dt_to_check >= datetime.time(13, 0, 0)) | (dt_to_check <= datetime.time(15, 0, 0))
        return b

    def get_next_call_date_time(self):
        return self.next_bar_close

    def do_call(self):
        end_time = self.next_bar_close
        self._update_next_bar_close()
        bar_dict = {}
        local_end_time = to_cn_market_time(end_time)
        if not self._is_trade_time(local_end_time.time()):
            return

        for ticker in self.tickers:
            if not self.ticker_dict[ticker].is_empty():
                bar_dict[ticker] = build_bar(local_end_time, self.ticker_dict[ticker])

        if len(bar_dict):
            bars = Bars(bar_dict)
            self.queue.put((self.on_bar_event, bars))

    def load_data(self):
        """
        Overwrite this for new source data structures
        """
        try:
            df = self.live_quote_arg_func(self.tickers)
            for index, ticker in enumerate(self.tickers):
                ticker_info = df.loc[index]
                self.ticker_dict[ticker].append(ticker_info['price'],
                                                ticker_info['volume'],
                                                ticker_info['amount'],
                                                ticker_info['time'])
        except Exception:
            raise ValueError('Polling thread exception')
