# -*- coding: utf-8 -*-


import time
import logging

from . import __logger__

logger = logging.getLogger(__logger__)


def timeit(func):
    """
    https://github.com/vex1023/vxUtils/blob/master/vxUtils/decorator.py
    @timeit
    def test():
        time.sleep(1)
    """

    def wrapper(*args, **kwargs):
        _start = time.time()
        retval = func(*args, **kwargs)
        _end = time.time()
        logger.info('function %s() used : %.6f s' % (func.__name__, _end - _start))
        return retval

    return wrapper
