""" ./examples/label/suite/module_level_custom_suite.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_suite


def test_module_custom_suite(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_module_level_custom_suite",
                              has_suite("module level suite name"),
                              )
                )
