import pytest

import allure_commons
from allure_commons.model2 import Label

from .utils import ALLURE_TITLE_MARK
from .utils import ALLURE_DESCRIPTION_MARK
from .utils import ALLURE_DESCRIPTION_HTML_MARK
from .utils import ALLURE_LABEL_MARK


class AllurePytestBddApi:
    def __init__(self, lifecycle):
        self.lifecycle = lifecycle

    @allure_commons.hookimpl
    def decorate_as_title(self, test_title):
        allure_title_mark = getattr(pytest.mark, ALLURE_TITLE_MARK)
        return allure_title_mark(test_title)

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
            test_result.labels.extend(Label(name=label_type, value=value) for value in labels or [])
