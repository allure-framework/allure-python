import sys
import time
import uuid
import inspect
import hashlib


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


def func_parameters(func, *a, **kw):
    if sys.version_info.major < 3:
        all_names = inspect.getargspec(func).args
        defaults = inspect.getargspec(func).defaults
    else:
        all_names = inspect.getfullargspec(func).args
        defaults = inspect.getfullargspec(func).defaults
    args_part = [(n, str(v)) for n, v in zip(all_names, a)]
    kwarg_part = [(n, str(kw[n]) if n in kw else str(defaults[i])) for i, n in enumerate(all_names[len(a):])]
    return args_part + kwarg_part
