# -*- coding: utf-8 -*-

import numpy as np


def dual_thrust(open_price, low_series, high_series, close_series, **kwargs):
    up_length = kwargs.get('up_length', 1)
    up_coeff = kwargs.get('up_coeff', 1)
    down_length = kwargs.get('down_length', 1)
    down_coeff = kwargs.get('down_coeff', 1)

    # 上轨-Min最低价
    up_min_low = np.min(low_series[-up_length:])

    # 上轨-Min收盘价
    up_min_close = np.min(close_series[-up_length:])

    # 上轨-Max收盘价
    up_max_close = np.max(close_series[-up_length:])

    # 上轨-Max最高价
    up_max_high = np.max(high_series[-up_length:])

    # 下轨-Min最低价
    down_min_low = np.min(low_series[-down_length:])

    # 下轨-Min收盘价
    down_min_close = np.min(close_series[-down_length:])

    # 下轨-Max收盘价
    down_max_close = np.max(close_series[-down_length:])

    # 下轨-Max最高价
    down_max_high = np.max(high_series[-down_length:])

    up_thurst = open_price + up_coeff * max(up_max_close - up_min_low, up_max_high - up_min_close)
    down_thrust = open_price - down_coeff * max(down_max_close - down_min_low, down_max_high - down_min_close)

    return up_thurst, down_thrust
