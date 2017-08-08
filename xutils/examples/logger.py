# -*- coding: utf-8 -*-


from xutils.custom_logger import CustomLogger

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='test.log')
LOGGER.info('Hello world')
LOGGER.set_level('critical')
LOGGER.info('Hello world')
