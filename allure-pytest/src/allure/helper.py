import pytest
from functools import wraps

from allure.utils import uuid4
from allure.constants import Severity
from allure.constants import ALLURE_LABEL_PREFIX, ALLURE_LINK_PREFIX
from allure.constants import LabelType, LinkType, AttachmentType


class AllureTestHelper(object):

    def __init__(self, config):
        self.config = config
        self.attach = Attach(config)

    def label(self, label_type, *value):
        allure_label = getattr(pytest.mark, '{prefix}.{label_type}'.format(prefix=ALLURE_LABEL_PREFIX,
                                                                           label_type=label_type))
        return allure_label(*value, label_type=label_type)

    def severity(self, severity):
        return self.label(LabelType.SEVERITY, severity.value)

    @property
    def severity_level(self):
        return Severity

    def feature(self, *features):
        return self.label(LabelType.FEATURE, *features)

    def story(self, *stories):
        return self.label(LabelType.STORY, *stories)

    def link(self, url, link_type=LinkType.LINK, name=None):
        allure_link = getattr(pytest.mark, '{prefix}.{link_type}'.format(prefix=ALLURE_LINK_PREFIX,
                                                                         link_type=link_type))
        return allure_link(url, name=name)

    def issue(self, url, name=None):
        return self.link(url, link_type=LinkType.ISSUE, name=name)

    def test_case(self, url, name=None):
        return self.link(url, link_type=LinkType.TEST_CASE, name=name)

    def step(self, title):
        if callable(title):
            return LazyInitStepContext(self, title.__name__)(title)
        else:
            return LazyInitStepContext(self, title)

    @pytest.hookimpl()
    def pytest_namespace(self):
        return {"allure": self}


class StepContext:

    def __init__(self, allure, title):
        self.allure = allure
        self.title = title
        self._uuid = uuid4()

    def __enter__(self):
        self.allure.config.hook.pytest_allure_before_step(uuid=self._uuid,
                                                          title=self.title)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.allure.config.hook.pytest_allure_after_step(uuid=self._uuid,
                                                         title=self.title,
                                                         exc_type=exc_type,
                                                         exc_val=exc_val,
                                                         exc_tb=exc_tb)

    def __call__(self, func):
        @wraps(func)
        def impl(*a, **kw):
            __tracebackhide__ = True
            with StepContext(self.allure, self.title.format(*a, **kw)):
                return func(*a, **kw)
        return impl


class LazyInitStepContext(StepContext):

    def __init__(self, allure_helper, title):
        self.allure_helper = allure_helper
        self.title = title
        self._uuid = uuid4()

    @property
    def allure(self):
        return self.allure_helper


class Attach(object):

    def __init__(self, config):
        self.config = config

        def imp(attachment_type):
            def attach(source, name=None):
                self(source, attachment_type.mime_type, attachment_type.extension, name=name)
            return attach

        for preset in list(AttachmentType):
            self.__dict__[preset.extension] = imp(preset)

    def __call__(self, source, mime_type, extension, name=None):
        self.config.hook.pytest_allure_attach(name=name, source=source, mime_type=mime_type, extension=extension)

    def data(self, body, mime_type, extension, name=None):
        raise NotImplementedError
