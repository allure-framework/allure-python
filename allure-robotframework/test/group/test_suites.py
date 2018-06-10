import unittest
import os

from allure_commons_test.report import AllureReport, has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.label import has_label
from hamcrest import assert_that, has_entry


def has_sub_suite(suite):
    return has_label('subSuite', suite)


def has_suite(suite):
    return has_label('suite', suite)


def has_parent_suite(suite):
    return has_label('parentSuite', suite)


class TestSuites(unittest.TestCase):
    allure_report = AllureReport(os.environ.get('TEST_TMP', None))

    def test_single_suite(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Single Suite',
                has_container(
                    self.allure_report,
                    has_entry(
                        'name', 'Case With Single Suite'),
                    has_container(
                        self.allure_report,
                        has_entry(
                            'name', 'Single Suite'))
                ),
                has_suite('Single Suite')
            )
        )

    def test_double_suite(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Two Parent Suites',
                has_container(
                    self.allure_report,
                    has_entry(
                        'name', 'Case With Two Parent Suites'),
                    has_container(
                        self.allure_report,
                        has_entry(
                            'name', 'Suite With One Parent'),
                        has_container(
                            self.allure_report,
                            has_entry('name', 'First Level Suite')
                        )
                    )
                ),
                has_sub_suite('Suite With One Parent'),
                has_suite('First Level Suite'),
            )
        )

    def test_triple_suite(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Three Parent Suites',
                has_container(
                    self.allure_report,
                    has_entry(
                        'name', 'Case With Three Parent Suites'),
                    has_container(
                        self.allure_report,
                        has_entry(
                            'name', 'Suite With Two Parent'),
                        has_container(
                            self.allure_report,
                            has_entry(
                                'name', 'Second Level Suite'),
                            has_container(
                                self.allure_report,
                                has_entry('name', 'First Level Suite')
                            )
                        )
                    )
                ),
                has_sub_suite('Suite With Two Parent'),
                has_suite('Second Level Suite'),
                has_parent_suite('First Level Suite')
            )
        )

    def test_quadruple_suite(self):
        assert_that(
            self.allure_report,
            has_test_case(
                'Case With Four Parent Suites',
                has_container(
                    self.allure_report,
                    has_entry('name', 'Case With Four Parent Suites'),
                    has_container(
                        self.allure_report,
                        has_entry('name', 'Suite With Three Parent'),
                        has_container(
                            self.allure_report,
                            has_entry('name', 'Third Level Suite'),
                            has_container(
                                self.allure_report,
                                has_entry('name', 'Second Level Suite'),
                                has_container(
                                    self.allure_report,
                                    has_entry('name', 'First Level Suite')
                                )
                            )
                        )
                    )
                ),
                has_sub_suite('Third Level Suite.Suite With Three Parent'),
                has_suite('Second Level Suite'),
                has_parent_suite('First Level Suite')
            )
        )
