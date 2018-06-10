import unittest
import os

from allure_robotframework.constants import RobotBasicKeywords
from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.result import with_status, has_step
from hamcrest import assert_that


class StepStatus(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_passed_with_step(self):
        assert_that(self.allure_report, has_test_case('Passed Case With Step',
                                                      with_status('passed'),
                                                      has_step(RobotBasicKeywords.NO_OPERATION,
                                                               with_status('passed')
                                                               )
                                                      )
                    )

    def test_passed_with_multiple_step(self):
        assert_that(self.allure_report, has_test_case('Passed Case With Multiple Step',
                                                      with_status('passed'),
                                                      has_step('Passed Keyword 1',
                                                               with_status('passed'),
                                                               has_step(RobotBasicKeywords.NO_OPERATION,
                                                                        with_status('passed')
                                                                        )
                                                               ),
                                                      has_step('Passed Keyword 2',
                                                               with_status('passed'),
                                                               has_step(RobotBasicKeywords.NO_OPERATION,
                                                                        with_status('passed')
                                                                        )
                                                               ),
                                                      )
                    )
