import unittest
import os

from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.result import has_description
from hamcrest import assert_that


class TestSuites(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_case_with_description(self):
        assert_that(self.allure_report,
                    has_test_case('Case With Description',
                                  has_description('Case description')
                                  )
                    )

    def test_case_with_dynamyc_description(self):
        assert_that(self.allure_report,
                    has_test_case('Case With Dynamic Description',
                                  has_description('End description')
                                  )
                    )
