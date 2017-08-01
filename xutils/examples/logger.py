# -*- coding: utf-8 -*-


from xutils.custom_logger import CustomLogger

LOGGER = CustomLogger(log_level='info')
LOGGER.info('Hello world')
LOGGER.set_level('critical')
LOGGER.info('Hello world')
