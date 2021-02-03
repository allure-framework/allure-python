from robot.api import SuiteVisitor
from allure_commons.utils import get_testplan
from allure_robotframework.utils import allure_labels
from allure_commons.types import LabelType


# noinspection PyPep8Naming
class allure_testplan(SuiteVisitor):
    def __init__(self):
        self.testplan = get_testplan()
        self.allure_ids = [test["id"] for test in self.testplan] if self.testplan else []
        self.selectors = [test["selector"] for test in self.testplan] if self.testplan else []

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
