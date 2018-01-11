# -*- coding: utf-8 -*-

from xutils.bar_builder.bar import (BasicBar,
                                    BarFrequency)


def build_bar(trade_date, price, volume_, amount_):
    open_ = float(price[0])
    high = float(max(price))
    low = float(min(price))
    close = float(price[-1])
    volume = sum(int(v) for v in volume_)
    amount = sum(float(a) for a in amount_)

    return BasicBar(trade_date, open_, high, low, close, volume, None, BarFrequency.DAY, amount)
