from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title


def test_dynamic_display_name(executed_docstring_path):
    """ ./examples/display_name/dynamic_display_name.rst """

    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_dynamic_display_name",
                              has_title("It is renamed test")
                              )
                )
