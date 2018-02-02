# -*- coding: utf-8 -*-


from toolz.compatibility import itervalues
from toolz.dicttoolz import itemfilter


def valid_dict(d, keys=None):
    """
    检查是否字典中含有值为None的键(给定键的名称则检查给定的键，如果没有，则检查全部键)
    - 如果没有值为None的键，则返回True，反之False
    - 如果keys中的键不存在于d中，也返回False
    """

    if keys is None:
        d_ = d
    else:
        d_ = itemfilter(lambda item: item[0] in keys, d)
        if len(d_) != len(keys):
            return False
    values = list(itervalues(d_))
    return False if None in values else True
