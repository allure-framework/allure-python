import pytest

import allure_commons

from allure_commons.model2 import Label
from allure_commons.model2 import Link
from allure_commons.model2 import Parameter
from allure_commons.utils import represent

from .utils import ALLURE_DESCRIPTION_HTML_MARK
from .utils import ALLURE_DESCRIPTION_MARK
from .utils import ALLURE_LABEL_MARK
from .utils import ALLURE_LINK_MARK
from .utils import ALLURE_TITLE_ATTR

from .utils import apply_link_pattern
from .utils import attach_data
from .utils import attach_file
from .utils import get_link_patterns
from .steps import start_step
from .steps import stop_step


class AllurePytestBddApiHooks:
    def __init__(self, config, lifecycle):
        self.lifecycle = lifecycle
        self.__link_patterns = get_link_patterns(config)

    @allure_commons.hookimpl
    def decorate_as_title(self, test_title):

        def decorator(fn):
            setattr(fn, ALLURE_TITLE_ATTR, test_title)
            return fn

        return decorator

    @allure_commons.hookimpl
    def add_title(self, test_title):
        with self.lifecycle.update_test_case() as test_result:
            test_result.name = test_title

    @allure_commons.hookimpl
    def decorate_as_description(self, test_description):
        allure_description_mark = getattr(pytest.mark, ALLURE_DESCRIPTION_MARK)
        return allure_description_mark(test_description)

    @allure_commons.hookimpl
    def add_description(self, test_description):
        with self.lifecycle.update_test_case() as test_result:
            test_result.description = test_description

    @allure_commons.hookimpl
    def decorate_as_description_html(self, test_description_html):
        allure_description_html_mark = getattr(pytest.mark, ALLURE_DESCRIPTION_HTML_MARK)
        return allure_description_html_mark(test_description_html)

    @allure_commons.hookimpl
    def add_description_html(self, test_description_html):
        with self.lifecycle.update_test_case() as test_result:
            test_result.descriptionHtml = test_description_html

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        allure_label_mark = getattr(pytest.mark, ALLURE_LABEL_MARK)
        return allure_label_mark(*labels, label_type=label_type)

    @allure_commons.hookimpl
    def add_label(self, label_type, labels):
        with self.lifecycle.update_test_case() as test_result:
            test_result.labels.extend(
                Label(name=label_type, value=value) for value in labels or []
            )

    @allure_commons.hookimpl
    def decorate_as_link(self, url, link_type, name):
        url = apply_link_pattern(self.__link_patterns, link_type, url)
        allure_link_mark = getattr(pytest.mark, ALLURE_LINK_MARK)
        return allure_link_mark(url, name=name, link_type=link_type)

    @allure_commons.hookimpl
    def add_link(self, url, link_type, name):
        url = apply_link_pattern(self.__link_patterns, link_type, url)
        with self.lifecycle.update_test_case() as test_result:
            test_result.links.append(Link(url=url, name=name, type=link_type))

    @allure_commons.hookimpl
    def add_parameter(self, name, value, excluded, mode):
        with self.lifecycle.update_test_case() as test_result:
            test_result.parameters.append(
                Parameter(
                    name=name,
                    value=represent(value),
                    excluded=excluded,
                    mode=mode.value if mode else None,
                ),
            )

    @allure_commons.hookimpl
    def start_step(self, uuid, title, params):
        start_step(self.lifecycle, step_uuid=uuid, title=title, params=params)

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb):
        stop_step(
            self.lifecycle,
            uuid,
            exception=exc_val,
            exception_type=exc_type,
            traceback=exc_tb,
        )

    @allure_commons.hookimpl
    def attach_data(self, body, name, attachment_type, extension):
        attach_data(self.lifecycle, body, name, attachment_type, extension)

    @allure_commons.hookimpl
    def attach_file(self, source, name, attachment_type, extension):
        attach_file(self.lifecycle, source, name, attachment_type, extension)
