# -*- coding: utf-8 -*-


import time
import functools


def handle_exception(logger):
    """
    :param logger: logging, a logging object
    :return: decorator, wraps exception loggers
    """

    def decorator(query_func):
        @functools.wraps(query_func)
        def wrapper(*args, **kwargs):
            try:
                return query_func(*args, **kwargs)
            except Exception as e:
                logger.info('Exception in function {0} -- {1}'.format(query_func.__name__, e))

        return wrapper

    return decorator


def clock(logger):
    """
    :param logger: logging, a logging object
    :return: decorator, wraps time 
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _start = time.time()
            retval = func(*args, **kwargs)
            _end = time.time()
            logger.info('function {0} used : {1} s'.format(func.__name__, _end - _start))
            return retval

        return wrapper

    return decorator
