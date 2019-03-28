# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import allure_commons
from allure_pytest.utils import ALLURE_TITLE
from allure_pytest.utils import ALLURE_DESCRIPTION, ALLURE_DESCRIPTION_HTML
from allure_pytest.utils import ALLURE_LABEL_PREFIX, ALLURE_LINK_PREFIX


class AllureTestHelper(object):

    def __init__(self, config):
        self.config = config

    @allure_commons.hookimpl
    def decorate_as_title(self, test_title):
        allure_title = getattr(pytest.mark, ALLURE_TITLE)
        return allure_title(test_title)

    @allure_commons.hookimpl
    def decorate_as_description(self, test_description):
        allure_description = getattr(pytest.mark, ALLURE_DESCRIPTION)
        return allure_description(test_description)

    @allure_commons.hookimpl
    def decorate_as_description_html(self, test_description_html):
        allure_description_html = getattr(pytest.mark, ALLURE_DESCRIPTION_HTML)
        return allure_description_html(test_description_html)

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        allure_label_marker = '{prefix}.{label_type}'.format(prefix=ALLURE_LABEL_PREFIX, label_type=label_type)
        allure_label = getattr(pytest.mark, allure_label_marker)
        return allure_label(*labels, label_type=label_type)

    @allure_commons.hookimpl
    def decorate_as_link(self, url, link_type, name):
        allure_link_marker = '{prefix}.{link_type}:{postfix}'.format(
            prefix=ALLURE_LINK_PREFIX,
            link_type=link_type,
            postfix=url
        )
        pattern = dict(self.config.option.allure_link_pattern).get(link_type, u'{}')
        url = pattern.format(url)
        allure_link = getattr(pytest.mark, allure_link_marker)
        name = url if name is None else name
        return allure_link(url, name=name, link_type=link_type)
