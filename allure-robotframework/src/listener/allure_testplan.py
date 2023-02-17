from robot.api import SuiteVisitor
from allure_commons.utils import get_testplan
from allure_robotframework.utils import allure_labels
from allure_commons.types import LabelType


# noinspection PyPep8Naming
class allure_testplan(SuiteVisitor):
    def __init__(self):
        self.testplan = get_testplan()
        self.allure_ids = self.__to_set_by_item_key(self.testplan, "id")
        self.selectors = self.__to_set_by_item_key(self.testplan, "selector")

    @staticmethod
    def __to_set_by_item_key(items, key):
        return {item[key] for item in items if key in item}

    def start_suite(self, suite):
        if self.testplan:
            suite.tests = self.included_tests(suite)

    def included_tests(self, suite):
        included_tests = []

        for test in suite.tests:
            allure_id = None
            for label in allure_labels(test.tags):
                if label.name == LabelType.ID:
                    allure_id = str(label.value)
            if allure_id and allure_id in self.allure_ids:
                included_tests.append(test)
            elif test.longname in self.selectors:
                included_tests.append(test)

        return included_tests

    def end_suite(self, suite):
        suite.suites = [s for s in suite.suites if s.test_count > 0]
