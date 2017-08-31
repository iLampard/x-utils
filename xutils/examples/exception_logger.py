# -*- coding: utf-8 -*-


from xutils.custom_logger import CustomLogger
from xutils.decorators import handle_exception

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='test.log')


@handle_exception(logger=LOGGER)
def test_exception():
    raise ValueError('Error here blabla')


if __name__ == '__main__':
    test_exception()

