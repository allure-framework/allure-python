# -*- coding: utf-8 -*-
import sys
import time
import uuid
import inspect
import hashlib
import platform

from six import text_type


def md5(*args):
    m = hashlib.md5()
    for arg in args:
        part = arg.encode('utf-8')
        m.update(part)
    return m.hexdigest()


def uuid4():
    return str(uuid.uuid4())


def now():
    return int(round(1000 * time.time()))


def platform_label():
    major_version, _, __ = platform.python_version_tuple()
    implementation = platform.python_implementation()
    return '{implementation}{major_version}'.format(implementation=implementation.lower(),
                                                    major_version=major_version)


def represent(item):
    """
    >>> represent(None)
    'None'

    >>> represent(123)
    '123'

    >>> represent('hi') == u"'hi'"
    True

    >>> represent(u'привет') == u"'привет'"
    True

    >>> from sys import version_info
    >>> represent(str(bytearray([0xd0, 0xbf]))) == u"'\u043f'" if version_info.major < 3 else True
    True

    >>> from struct import pack
    >>> result = "<type 'str'>" if version_info.major < 3 else "<class 'bytes'>"
    >>> represent(pack('h', 0x89)) == result
    True

    >>> result = "<type 'int'>" if version_info.major < 3 else "<class 'int'>"
    >>> represent(int) == result
    True

    >>> represent(represent)  # doctest: +ELLIPSIS
    '<function represent at ...>'

    >>> represent([represent])  # doctest: +ELLIPSIS
    '[<function represent at ...>]'

    >>> class ClassWithName(object):
    ...     pass

    >>> represent(ClassWithName)
    "<class 'utils.ClassWithName'>"
    """

    if sys.version_info.major < 3 and isinstance(item, str):
        try:
            item = item.decode(encoding='UTF-8')
        except UnicodeDecodeError:
            pass

    if isinstance(item, text_type):
        return u'\'%s\'' % item
    elif isinstance(item, (bytes, bytearray)):
        return repr(type(item))
    else:
        return repr(item)


def func_parameters(func, *a, **kw):
    bowels = inspect.getargspec(func) if sys.version_info.major < 3 else inspect.getfullargspec(func)
    args_dict = dict(zip(bowels.args, map(represent,  a)))
    kwargs_dict = dict(zip(kw, list(map(lambda i: represent(kw[i]), kw))))
    kwarg_defaults = dict(zip(reversed(bowels.args), reversed(list(map(represent, bowels.defaults or ())))))
    kwarg_defaults.update(kwargs_dict)
    return args_dict, kwarg_defaults
