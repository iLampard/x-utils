# -*- coding: utf-8 -*-
try:
    from Queue import (Empty,
                       Queue)
except ImportError:
    from queue import (Empty,
                       Queue)
from argcheck import *
from xutils.bar_builder.polling_thread import BarThread


class LiveFeed(object):
    def __init__(self, tickers, frequency, live_quote_arg_func, **kwargs):
        self.tickers = tickers
        self.frequency = frequency
        self.inquery_period = kwargs.get('inquery_period', 1)
        self.on_bar_event = kwargs.get('on_bar_event', 1)
        self.queue_timeout = kwargs.get('queue_timeout', 0.01)
        self.queue = Queue()
        self.thread = BarThread(tickers=tickers,
                                inquery_period=self.inquery_period,
                                frequency=frequency,
                                queue=self.queue,
                                live_quote_arg_func=live_quote_arg_func,
                                on_bar_event=self.on_bar_event)

    def start(self):
        if self.thread.is_alive():
            raise Exception('Thread already started')
        self.thread.start()
        return

    def stop(self):
        self.thread.stop()
        return

    def join(self):
        if self.thread.is_alive():
            self.thread.join()
        return

    def eof(self):
        return self.thread.stopped()

    def get_next_bar(self):
        ret = None
        try:
            event_type, event_data = self.queue.get(block=True, timeout=self.queue_timeout)
            if event_type == self.on_bar_event:
                ret = event_data
            else:
                raise Exception('Invalid event received: {0} - {1}'.format(event_type, event_data))
        except Empty:
            pass

        return ret
