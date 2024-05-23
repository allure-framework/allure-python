import pytest
import allure_commons
from .utils import ALLURE_DESCRIPTION_MARK, ALLURE_DESCRIPTION_HTML_MARK
from .utils import ALLURE_LABEL_MARK, ALLURE_LINK_MARK
from .utils import format_allure_link


class AllureTestHelper:
    def __init__(self, config):
        self.config = config

    @allure_commons.hookimpl
    def decorate_as_description(self, test_description):
        allure_description = getattr(pytest.mark, ALLURE_DESCRIPTION_MARK)
        return allure_description(test_description)

    @allure_commons.hookimpl
    def decorate_as_description_html(self, test_description_html):
        allure_description_html = getattr(pytest.mark, ALLURE_DESCRIPTION_HTML_MARK)
        return allure_description_html(test_description_html)

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        allure_label = getattr(pytest.mark, ALLURE_LABEL_MARK)
        return allure_label(*labels, label_type=label_type)

    @allure_commons.hookimpl
    def decorate_as_link(self, url, link_type, name):
        url = format_allure_link(self.config, url, link_type)
        allure_link = getattr(pytest.mark, ALLURE_LINK_MARK)
        name = url if name is None else name
        return allure_link(url, name=name, link_type=link_type)
