# -*- coding: utf-8 -*-


from xutils.decorators import clock
from xutils.custom_logger import CustomLogger

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='clock.log')


@clock(LOGGER)
def test_calc():
    sum = 0
    for i in range(100000):
        sum += i
    return


test_calc()
