from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_severity


def test_severity(executed_docstring_path):
    """ ./examples/label/severity/severity.rst """

    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_severity",
                              has_severity("minor"),
                              )
                )
