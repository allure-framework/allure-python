from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label


def test_allure_manual_label(executed_docstring_path):
    """ ./examples/label/manual/allure_manual.rst """
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_manual",
                              has_label("ALLURE_MANUAL", True)
                              )
                )


def test_allure_manual_label_dynamic(executed_docstring_path):
    """ ./examples/label/manual/allure_manual.rst """
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_manual_dynamic",
                              has_label("ALLURE_MANUAL", True)
                              ),
                )
