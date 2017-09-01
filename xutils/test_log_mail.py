# -*- coding: utf-8 -*-


from xutils.custom_logger import CustomLogger
from xutils.decorators import handle_exception

LOGGER = CustomLogger(logger_name='TestLogger', log_level='info', log_file='test.log')
server = {'name':'smtp.163.com','user':'','passwd':''}
fromAddr = ''
toAddr = ['']  
subject = u'logging_test'


@handle_exception(logger=LOGGER, server = server, fromAddr = fromAddr, toAddr = toAddr, subject =subject)
def test_exception():
    raise ValueError('Error here blabla')


if __name__ == '__main__':
    test_exception()
    
    


    
    