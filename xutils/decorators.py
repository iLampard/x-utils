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


def _email_params(**kwargs):
    subject = kwargs.get('subject', None)
    text = kwargs.get('text', None)
    sender = kwargs.get('sender', None)
    username = kwargs.get('username', None)
    password = kwargs.get('password', None)
    host = kwargs.get('host', None)
    receiver = kwargs.get('receiver', None)
    return {'subject': subject, 'text': text, 'sender': sender, 'username': username, 'password': password,
            'host': host, 'receiver': receiver}


def handle_exception(logger, **email_params):
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
                params = _email_params(**email_params)
                if params['subject'] is not None:
                    logger.info('Now is sending the email with exception message')
                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    msg = t + ' ' + 'Exception in function {0} -- {1}'.format(query_func.__name__, e)
                    _send(subject=params['subject'],
                          text=msg,
                          sender=params['sender'],
                          username=params['username'],
                          password=params['password'],
                          host=params['host'],
                          receiver=params['receiver'])
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
