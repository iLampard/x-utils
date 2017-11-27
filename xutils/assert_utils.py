# -*- coding: utf-8 -*-


import warnings


def py_assert(condition, exception, msg=''):
    if not condition:
        raise exception(msg)


def py_warning(condition, warn_type, msg=''):
    if not condition:
        warnings.warn(msg, warn_type)
