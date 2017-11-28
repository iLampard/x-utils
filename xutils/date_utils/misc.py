# -*- coding: utf-8 -*-

from time import (mktime,
                  strptime)


def is_within_hour_range(ref_time, start_time, end_time):
    """
    :param ref_time: datetime/string, 需要判断的时间变量
    :param start_time: string, 时间区间上限
    :param end_time: string, 时间下限
    :return: 判断某个时间是否在限定的时间范围内
    """
    str_ref_time = ref_time.strftime('%Y%m%d')
    start_time_ = mktime(strptime(str_ref_time + '-' + start_time, '%Y%m%d-%H:%M'))
    end_time_ = mktime(strptime(str_ref_time + '-' + end_time, '%Y%m%d-%H:%M'))
    ref_time_ = mktime(ref_time.timetuple())
    if start_time_ <= ref_time_ <= end_time_:
        return True
    else:
        return False
