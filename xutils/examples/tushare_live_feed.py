# -*- coding: utf-8 -*-


from xutils.bar_builder import (LiveFeed,
                                BarFrequency)
import tushare as ts


if __name__ == '__main__':
    live_feed = LiveFeed(tickers=['zh500'],
                         frequency=BarFrequency.MINUTE,
                         live_quote_arg_func=ts.get_realtime_quotes)
    live_feed.start()
    while not live_feed.eof():
        bars = live_feed.get_next_bar()
        if bars is not None:
            print(bars['zh500'].date_time, bars['zh500'].price)

