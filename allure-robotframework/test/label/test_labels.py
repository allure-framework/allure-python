import unittest
import os

from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.label import has_tag, has_label
from allure_commons_test.result import has_history_id
from hamcrest import assert_that


class CaseStatus(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_tags(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Tags',
                has_tag('my_awesome_tag'),
                has_tag('another_awesome_tag')
            )
        )

    def test_threads(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Thread #0',
                has_label('thread', 'Thread #0')
            ),
            has_test_case(
                'Case With Thread #1',
                has_label('thread', 'Thread #1')
            )
        )

    def test_history_id(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Tags',
                has_history_id()
            )
        )
