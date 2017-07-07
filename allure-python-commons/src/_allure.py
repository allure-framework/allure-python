from functools import partial
from functools import wraps

from allure_commons._core import plugin_manager
from allure_commons.types import LabelType, LinkType
from allure_commons.utils import uuid4
from allure_commons.utils import func_parameters


def safely(result):
    if result:
        return result[0]
    else:
        def dummy(function):
            return function
        return dummy


def label(label_type, *labels):
    return safely(plugin_manager.hook.decorate_as_label(label_type=label_type, labels=labels))


def severity(severity_level):
    return label(LabelType.SEVERITY, severity_level)


def tag(*tags):
    return label(LabelType.TAG, *tags)


def feature(*features):
    return label(LabelType.FEATURE, *features)


def story(*stories):
    return label(LabelType.STORY, *stories)


def link(url, link_type=LinkType.LINK, name=None):
    return safely(plugin_manager.hook.decorate_as_link(url=url, link_type=link_type, name=name))


def issue(url, name=None):
    return link(url, link_type=LinkType.ISSUE, name=name)


def testcase(url, name=None):
    return link(url, link_type=LinkType.TEST_CASE, name=name)


def add_label(label_type, labels):
    print("Y"*29)


def add_link(url, link_type=LinkType.LINK, name=None):
    print ("X"*23)


class Dynamic(object):
    label = partial(add_label)
    severity = partial(add_label, LabelType.SEVERITY)
    tag = partial(add_label, LabelType.TAG)
    feature = partial(add_label, LabelType.FEATURE)
    story = partial(add_label, LabelType.STORY)

    link = partial(add_link)
    issue = partial(add_link, link_type=LinkType.ISSUE)
    testcase = partial(add_link, link_type=LinkType.TEST_CASE)


def step(title):
    if callable(title):
        return StepContext(title.__name__, [])(title)
    else:
        return StepContext(title, [])


class StepContext:

    def __init__(self, title, params):
        self.title = title
        self.params = params
        self.uuid = uuid4()

    def __enter__(self):
        plugin_manager.hook.start_step(uuid=self.uuid, title=self.title, params=self.params)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plugin_manager.hook.stop_step(uuid=self.uuid, title=self.title, exc_type=exc_type, exc_val=exc_val,
                                      exc_tb=exc_tb)

    def __call__(self, func):
        @wraps(func)
        def impl(*a, **kw):
            __tracebackhide__ = True
            params = func_parameters(func, *a, **kw)
            with StepContext(self.title.format(*a, **kw), params):
                return func(*a, **kw)
        return impl


class Attach(object):

    def __call__(self, body, name=None, attachment_type=None, extension=None):
        plugin_manager.hook.attach_data(body=body, name=name, attachment_type=attachment_type, extension=extension)

    def file(self, source, name=None, attachment_type=None, extension=None):
        plugin_manager.hook.attach_file(source=source, name=name, attachment_type=attachment_type, extension=extension)


attach = Attach()


class fixture(object):
    def __init__(self, fixture_function, parent_uuid=None, name=None):
        self._fixture_function = fixture_function
        self._parent_uuid = parent_uuid
        self._name = name if name else fixture_function.__name__
        self._uuid = uuid4()

    def __call__(self, *args, **kwargs):
        with self:
            return self._fixture_function(*args, **kwargs)

    def __enter__(self):
        plugin_manager.hook.start_fixture(parent_uuid=self._parent_uuid, uuid=self._uuid, name=self._name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        plugin_manager.hook.stop_fixture(uuid=self._uuid, exc_type=exc_type, exc_val=exc_val, exc_tb=exc_tb)
