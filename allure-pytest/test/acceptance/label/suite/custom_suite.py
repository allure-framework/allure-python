""" ./examples/label/suite/custom_suite.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_suite, has_parent_suite, has_sub_suite


def test_custom_suite(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_custom_suite",
                              has_suite("suite name"),
                              has_parent_suite("parent suite name"),
                              has_sub_suite("sub suite name")
                              )
                )
