from traceback import format_exception_only
from allure_commons.model2 import StatusDetails, Label
from allure_commons.model2 import Parameter
from allure_commons.utils import represent
from nose2 import util
import inspect

# ToDo move to commons
ALLURE_LABELS = [
    'epic',
    'feature',
    'story',
]


def timestamp_millis(timestamp):
    return int(timestamp * 1000)


def status_details(event):
    message, trace = None, None
    if event.exc_info:
        exc_type, value, _ = event.exc_info
        message = '\n'.join(format_exception_only(exc_type, value)) if exc_type or value else None
        trace = ''.join(util.exc_info_to_string(event.exc_info, event.test))
    elif event.reason:
        message = event.reason

    if message or trace:
        return StatusDetails(message=message, trace=trace)


def update_attrs(test, name, values):
    if type(values) in (list, tuple, str) and name.isidentifier():
        attrib = getattr(test, name, values)
        if attrib and attrib != values:
            attrib = sum(
                [tuple(i) if type(i) in (tuple, list) else (i,) for i in (attrib, values)],
                ()
            )
        setattr(test, name, attrib)


def labels(test):

    def _get_attrs(obj, keys):
        pairs = set()
        for key in keys:
            values = getattr(obj, key, ())
            for value in (values,) if type(values) == str else values:
                pairs.add((key, value))
        return pairs

    keys = ALLURE_LABELS
    pairs = _get_attrs(test, keys)

    if hasattr(test, "_testFunc"):
        pairs.update(_get_attrs(test._testFunc, keys))
    elif hasattr(test, "_testMethodName"):
        test_method = getattr(test, test._testMethodName)
        pairs.update(_get_attrs(test_method, keys))
    return [Label(name=name, value=value) for name, value in pairs]


def name(event):
    full_name = fullname(event)
    test_params = params(event)
    allure_name = full_name.split(".")[-1]
    if test_params:
        params_str = "-".join([p.value for p in test_params])
        return "{name}[{params_str}]".format(name=allure_name, params_str=params_str)
    return allure_name


def fullname(event):
    if hasattr(event.test, "_testFunc"):
        test_module = event.test._testFunc.__module__
        test_name = event.test._testFunc.__name__
        return "{module}.{name}".format(module=test_module, name=test_name)
    test_id = event.test.id()
    return test_id.split(":")[0]


def params(event):
    def _params(names, values):
        return [Parameter(name=name, value=represent(value)) for name, value in zip(names, values)]

    test_id = event.test.id()

    if len(test_id.split("\n")) > 1:
        if hasattr(event.test, "_testFunc"):
            wrapper_arg_spec = inspect.getfullargspec(event.test._testFunc)
            arg_set, obj = wrapper_arg_spec.defaults
            test_arg_spec = inspect.getfullargspec(obj)
            args = test_arg_spec.args
            return _params(args, arg_set)
        elif hasattr(event.test, "_testMethodName"):
            method = getattr(event.test, event.test._testMethodName)
            wrapper_arg_spec = inspect.getfullargspec(method)
            obj, arg_set = wrapper_arg_spec.defaults
            test_arg_spec = inspect.getfullargspec(obj)
            args = test_arg_spec.args
            return _params(args[1:], arg_set)
