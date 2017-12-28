# -*- coding: utf-8 -*-


from xutils.custom_logger import CustomLogger
from xutils.decorators import handle_exception

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='test.log')


@handle_exception(logger=LOGGER)
def test_exception():
    raise ValueError('Error here blabla')


@handle_exception(logger=LOGGER,
                  subject=u"[更新失败！！]",
                  sender='xxxx',
                  username='xxxx',
                  password='000',
                  host='mail.xxx.com',
                  receiver=['XXXX@qq.com'])
def test_exception_with_email():
    raise ValueError('Error here blabla')


if __name__ == '__main__':
    test_exception_with_email()
