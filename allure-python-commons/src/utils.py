# -*- coding: utf-8 -*-

import os
import sys
import six
import time
import uuid
import socket
import inspect
import hashlib
import platform
import threading
import traceback

if sys.version_info.major > 2:
    from traceback import format_exception_only
else:
    from _compat import format_exception_only


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


def thread_tag():
    return '{0}-{1}'.format(os.getpid(), threading.current_thread().name)


def host_tag():
    return socket.gethostname()


def represent(item):
    """
    >>> represent(None)
    'None'

    >>> represent(123)
    '123'

    >>> from sys import version_info
    >>> expected = u"'hi'" if version_info.major < 3 else "'hi'"
    >>> represent('hi') == expected
    True

    >>> from sys import version_info
    >>> expected = u"'привет'" if version_info.major < 3 else "'привет'"
    >>> represent(u'привет') == expected
    True

    >>> represent(bytearray([0xd0, 0xbf]))  # doctest: +ELLIPSIS
    "<... 'bytearray'>"

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

    if isinstance(item, six.text_type):
        return u'\'%s\'' % item
    elif isinstance(item, (bytes, bytearray)):
        return repr(type(item))
    else:
        return repr(item)


def func_parameters(func, *a, **kw):
    bowels = inspect.getargspec(func) if sys.version_info.major < 3 else inspect.getfullargspec(func)
    args_dict = dict(zip(bowels.args, map(represent, a)))
    kwargs_dict = dict(zip(kw, list(map(lambda i: represent(kw[i]), kw))))
    kwarg_defaults = dict(zip(reversed(bowels.args), reversed(list(map(represent, bowels.defaults or ())))))
    kwarg_defaults.update(kwargs_dict)
    return args_dict, kwarg_defaults


def format_traceback(exc_traceback):
    return ''.join(traceback.format_tb(exc_traceback)) if exc_traceback else None


def format_exception(etype, value):
    """
    >>> import sys

    >>> try:
    ...     assert False, u'Привет'
    ... except AssertionError:
    ...     etype, e, _ = sys.exc_info()
    ...     format_exception(etype, e) # doctest: +ELLIPSIS
    'AssertionError: ...\\n'

    >>> try:
    ...     assert False, 'Привет'
    ... except AssertionError:
    ...     etype, e, _ = sys.exc_info()
    ...     format_exception(etype, e) # doctest: +ELLIPSIS
    'AssertionError: ...\\n'

    >>> try:
    ...    compile("bla u'Привет'", "fake.py", "exec")
    ... except SyntaxError:
    ...    etype, e, _ = sys.exc_info()
    ...    format_exception(etype, e) # doctest: +ELLIPSIS
    '  File "fake.py", line 1...SyntaxError: invalid syntax\\n'

    >>> try:
    ...    compile("bla 'Привет'", "fake.py", "exec")
    ... except SyntaxError:
    ...    etype, e, _ = sys.exc_info()
    ...    format_exception(etype, e) # doctest: +ELLIPSIS
    '  File "fake.py", line 1...SyntaxError: invalid syntax\\n'

    >>> from hamcrest import assert_that, equal_to

    >>> try:
    ...     assert_that('left', equal_to('right'))
    ... except AssertionError:
    ...     etype, e, _ = sys.exc_info()
    ...     format_exception(etype, e) # doctest: +ELLIPSIS
    "AssertionError: \\nExpected:...but:..."

    >>> try:
    ...     assert_that(u'left', equal_to(u'right'))
    ... except AssertionError:
    ...     etype, e, _ = sys.exc_info()
    ...     format_exception(etype, e) # doctest: +ELLIPSIS
    "AssertionError: \\nExpected:...but:..."
    """
    return '\n'.join(format_exception_only(etype, value)) if etype or value else None
