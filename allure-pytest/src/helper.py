# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import allure_commons
from allure_pytest.utils import ALLURE_DESCRIPTION_MARK, ALLURE_DESCRIPTION_HTML_MARK
from allure_pytest.utils import ALLURE_LABEL_MARK, ALLURE_LINK_MARK


class AllureTitleHelper(object):
    @allure_commons.hookimpl
    def decorate_as_title(self, test_title):
        def decorator(func):
            # pytest.fixture wraps function, so we need to get it directly
            if getattr(func, '__pytest_wrapped__', None):
                function = func.__pytest_wrapped__.obj
            else:
                function = func
            function.__allure_display_name__ = test_title
            return func

        return decorator


class AllureTestHelper(object):
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
        pattern = dict(self.config.option.allure_link_pattern).get(link_type, u'{}')
        url = pattern.format(url)
        allure_link = getattr(pytest.mark, ALLURE_LINK_MARK)
        name = url if name is None else name
        return allure_link(url, name=name, link_type=link_type)
