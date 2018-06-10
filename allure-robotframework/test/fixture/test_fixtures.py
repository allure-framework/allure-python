import unittest
import os

from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.container import has_after, has_before, has_container
from hamcrest import assert_that, all_of


class TestSuites(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_case_with_setup(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Test Setup',
                has_container(
                    self.allure_report,
                    has_before('Test Setup Keyword')
                )
            ),
        )

    def test_case_with_teardown(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Test Teardown',
                has_container(
                    self.allure_report,
                    has_after('Test Teardown Keyword')
                )
            ),
        )

    def test_case_with_fixtures(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Test Fixtures',
                has_container(
                    self.allure_report,
                    all_of(
                        has_before('Test Setup Keyword'),
                        has_after('Test Teardown Keyword')
                    )
                )
            ),
        )

    def test_group_without_test_fixtures(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case Without Test Fixtures',
                has_container(
                    self.allure_report,
                    has_container(
                        self.allure_report,
                        all_of(
                            has_before('Suite Setup Keyword'),
                            has_after('Suite Teardown Keyword')
                        )
                    )
                )
            ),
        )

    def test_group_with_test_setup(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Test Setup',
                has_container(
                    self.allure_report,
                    has_container(
                        self.allure_report,
                        all_of(
                            has_before('Suite Setup Keyword'),
                            has_after('Suite Teardown Keyword')
                        )
                    ),
                    has_before('Test Setup Keyword')
                )
            ),
        )

    def test_group_with_test_teardown(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Test Teardown',
                has_container(
                    self.allure_report,
                    has_container(
                        self.allure_report,
                        all_of(
                            has_before('Suite Setup Keyword'),
                            has_after('Suite Teardown Keyword')
                        )
                    ),
                    has_after('Test Teardown Keyword')
                )
            ),
        )

    def test_group_with_test_fixtures(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Test Fixtures',
                has_container(
                    self.allure_report,
                    has_container(
                        self.allure_report,
                        all_of(
                            has_before('Suite Setup Keyword'),
                            has_after('Suite Teardown Keyword')
                        )
                    ),
                    all_of(
                        has_before('Test Setup Keyword'),
                        has_after('Test Teardown Keyword')
                    )
                )
            ),
        )
