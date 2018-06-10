import unittest
import os

from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.result import has_link
from allure_commons.types import LinkType
from hamcrest import assert_that


class CaseMetadata(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_tags(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case In Suite With Metadata',
                has_link('https://google.com', LinkType.LINK, 'Link')
            )
        )
