# -*- coding: utf-8 -*-


import time
import functools
import smtplib
from email.mime.text import MIMEText


def _send(subject, text, sender, username, password, host, receiver):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = subject
    smtp = smtplib.SMTP()
    smtp.connect(host)
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def handle_exception(logger, **kw_decorator):
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
                if kw_decorator['subject'] is not None:
                    logger.info('Now is sending the email with exception message')
                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    msg = t + ' ' + 'Exception in function {0} -- {1}'.format(query_func.__name__, e)
                    _send(subject=kw_decorator['subject'],
                          text=msg,
                          sender=kw_decorator['sender'],
                          username=kw_decorator['username'],
                          password=kw_decorator['password'],
                          host=kw_decorator['host'],
                          receiver=kw_decorator['receiver'])
                    logger.info('Email is sent')

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
