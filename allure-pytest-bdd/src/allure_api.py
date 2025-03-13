import pytest

import allure_commons

from .utils import ALLURE_DESCRIPTION_MARK


class AllurePytestBddApi:
    def __init__(self, lifecycle):
        self.lifecycle = lifecycle

    @allure_commons.hookimpl
    def decorate_as_description(self, test_description):
        allure_description_mark = getattr(pytest.mark, ALLURE_DESCRIPTION_MARK)
        return allure_description_mark(test_description)

    @allure_commons.hookimpl
    def add_description(self, test_description):
        with self.lifecycle.update_test_case() as test_result:
            test_result.description = test_description
