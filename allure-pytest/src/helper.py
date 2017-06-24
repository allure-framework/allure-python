import pytest
from functools import wraps
from allure.utils import uuid4
from allure.types import Severity
from allure.types import LabelType, LinkType, AttachmentType

from allure_pytest.utils import step_parameters
from allure_pytest.utils import ALLURE_LABEL_PREFIX, ALLURE_LINK_PREFIX


class AllureTestHelper(object):

    def __init__(self, config):
        self.config = config
        self.attach = Attach(config)

    @property
    def attachment_type(self):
        return AttachmentType

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

        pattern = dict(self.config.option.allure_link_pattern).get(str(link_type), '{}')
        url = pattern.format(url)

        return allure_link(url, name=name)

    def issue(self, url, name=None):
        return self.link(url, link_type=LinkType.ISSUE, name=name)

    def testcase(self, url, name=None):
        return self.link(url, link_type=LinkType.TEST_CASE, name=name)

    def step(self, title):
        if callable(title):
            return LazyInitStepContext(self, title.__name__)(title)
        else:
            return LazyInitStepContext(self, title)

    def __getattr__(self, attr):
        for severity in Severity:
            if severity.name == attr:
                return self.severity(severity)

        for attach_type in AttachmentType:
            if attach_type.name == attr:
                return attach_type

        raise AttributeError

    @pytest.hookimpl()
    def pytest_namespace(self):
        return {"allure": self}


class StepContext:

    def __init__(self, allure, title, params):
        self.allure = allure
        self.title = title
        self._uuid = uuid4()
        self.params = params

    def __enter__(self):
        self.allure.config.hook.pytest_allure_before_step(uuid=self._uuid,
                                                          title=self.title,
                                                          params=self.params)

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
            params = step_parameters(func, *a, **kw)
            with StepContext(self.allure, self.title.format(*a, **kw), params):
                return func(*a, **kw)
        return impl


class LazyInitStepContext(StepContext):

    def __init__(self, allure_helper, title):
        self.allure_helper = allure_helper
        self.title = title
        self._uuid = uuid4()
        self.params = []

    @property
    def allure(self):
        return self.allure_helper


class Attach(object):

    def __init__(self, config):
        self.config = config

    def __call__(self, body, name=None,  attachment_type=None, extension=None):
        self.config.hook.pytest_allure_attach_data(body=body,
                                                   name=name,
                                                   attachment_type=attachment_type,
                                                   extension=extension)

    def file(self, source, name=None, attachment_type=None, extension=None):
        self.config.hook.pytest_allure_attach_file(source=source,
                                                   name=name,
                                                   attachment_type=attachment_type,
                                                   extension=extension)
