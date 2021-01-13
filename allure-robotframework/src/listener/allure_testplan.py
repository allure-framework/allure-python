from robot.api import SuiteVisitor
from allure_commons.utils import get_testplan
from allure_robotframework.utils import allure_labels
from allure_commons.types import LabelType


# noinspection PyPep8Naming
class allure_testplan(SuiteVisitor):
    def __init__(self):
        self.testplan = get_testplan()

    def start_suite(self, suite):
        if self.testplan:
            # included_tests = [test["selector"] for test in self.testplan]
            included_tests = self.included_tests(suite)
            if included_tests:
                suite.filter(included_tests=self.included_tests(suite))

    def included_tests(self, suite):
        included_tests = []
        for test in suite.tests:
            allure_id = None
            for label in allure_labels(test.tags):
                if label.name == LabelType.ID:
                    allure_id = str(label.value)
            if allure_id and any([allure_id == item.get("id", None) for item in self.testplan]):
                included_tests.append(test.name)

        return included_tests or [test["selector"] for test in self.testplan]
