# -*- coding: utf-8 -*-

# ref: https://github.com/tornadoweb/tornado/blob/master/tornado/util.py


import sys

PY3 = sys.version_info >= (3,)

# Aliases for types that are spelled differently in different Python
# versions. bytes_type is deprecated and no longer used in Tornado
# itself but is left in case anyone outside Tornado is using it.
bytes_type = bytes
if PY3:
    unicode_type = str
    basestring_type = str
else:
    # The names unicode and basestring don't exist in py3 so silence flake8.
    unicode_type = unicode  # noqa
    basestring_type = basestring  # noqa

__all__ = ['to_unicode']


_TO_UNICODE_TYPES = (unicode_type, type(None))


def to_unicode(value):
    """Converts a string argument to a unicode string.
    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")




