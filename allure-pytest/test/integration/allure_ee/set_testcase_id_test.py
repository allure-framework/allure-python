from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label


def test_set_testcase_id_label(executed_docstring_source):
    """
    >>> import allure

    >>> @allure.id(123)
    ... def test_allure_ee_id_label_example():
    ...     pass
    """
    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_allure_ee_id_label_example",
                              has_label("as_id", 123),
                              )
                )
