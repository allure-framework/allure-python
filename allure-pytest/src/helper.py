# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
import allure_commons
from allure_pytest.utils import ALLURE_LABEL_PREFIX, ALLURE_LINK_PREFIX


class AllureTestHelper(object):

    def __init__(self, config):
        self.config = config

    @allure_commons.hookimpl
    def decorate_as_label(self, label_type, labels):
        allure_label_marker = '{prefix}.{label_type}'.format(prefix=ALLURE_LABEL_PREFIX, label_type=label_type)
        allure_label = getattr(pytest.mark, allure_label_marker)
        return allure_label(*labels, label_type=label_type)

    @allure_commons.hookimpl
    def decorate_as_link(self, url, link_type, name):
        allure_link_marker = '{prefix}.{link_type}'.format(prefix=ALLURE_LINK_PREFIX, link_type=link_type)
        pattern = dict(self.config.option.allure_link_pattern).get(link_type, u'{}')
        url = pattern.format(url)
        allure_link = getattr(pytest.mark, allure_link_marker)
        return allure_link(url, name=name, link_type=link_type)
