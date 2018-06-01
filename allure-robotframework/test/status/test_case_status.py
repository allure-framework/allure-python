import unittest
import os

from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.result import with_status, has_status_details, with_status_message
from hamcrest import assert_that


class CaseStatus(unittest.TestCase):
    allure_report = AllureReport(os.path.join('output'))

    def test_passed(self):
        assert_that(self.allure_report, has_test_case('Passed Case', with_status('passed')))

    def test_failed(self):
        assert_that(self.allure_report, has_test_case('Failed Case', with_status('failed')))

    def test_failed_with_details(self):
        assert_that(self.allure_report, has_test_case('Failed Case With Message',
                                                      with_status('failed'),
                                                      has_status_details(with_status_message('Failed Details')
                                                                         )
                                                      )
                    )
