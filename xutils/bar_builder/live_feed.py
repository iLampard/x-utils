# -*- coding: utf-8 -*-

from Queue import (Empty,
                   Queue)


class LiveFeed(object):
    def __init__(self, tickers, frequency, thread, inquery_period):
        self.tickers = tickers
        self.thread = thread
        self.queue = Queue()
        self.inquery_period = inquery_period

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
            event_type, event_data = self.queue.get(True, self.inquery_period)
            if event_type == 1:
                ret = event_data
            else:
                raise ValueError('Invalid event received: {0} - {1}'.format(event_type, event_data))
        except Empty:
            pass

        return ret
