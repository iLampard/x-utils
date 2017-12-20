# -*- coding: utf-8 -*-


import time
import functools
import smtplib
from email.mime.text import MIMEText


def _send(*args, **kwargs):

    subject = kwargs.get('subject')
    email_dict = kwargs.get('email_dict')

    if email_dict is None:
        email_dict = kwargs

    host = email_dict['host']
    username = email_dict['username']
    password = email_dict['password']
    sender = email_dict['sender']
    receiver = email_dict.get('receiver')
    if receiver is None:
        receiver = email_dict['receiver']

    msg = MIMEText(email_dict['text'], 'plain', 'utf-8')
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

                subject = kw_decorator.get('subject')
                if subject is not None:  # 发送email

                    logger.info('Now is sending the email with exception message')
                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    msg = t + ' ' + 'Exception in function {0} -- {1}'.format(query_func.__name__, e)
                    email_dict = kw_decorator.get('email_dict')
                    if email_dict is not None:  # 用 email_dict 中的内容
                        pass
                    else:
                        email_dict = kw_decorator

                    email_dict['text'] = msg
                    _send(subject=subject, email_dict=email_dict)

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
