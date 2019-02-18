""" ./examples/label/custom/custom_label.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label


def test_custom_label(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_custom_label",
                              has_label("Application", "desktop"),
                              has_label("Application", "mobile")
                              )
                )
