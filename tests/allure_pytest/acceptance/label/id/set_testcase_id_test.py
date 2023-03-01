from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label


def test_set_testcase_id_label(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> @allure.id(123)
    ... def test_allure_ee_id_label_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_allure_ee_id_label_example",
            has_label("as_id", 123),
        )
    )


def test_set_dynamic_testcase_id_label(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_allure_ee_id_dynamic_label_example():
    ...     allure.dynamic.id(345)
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_allure_ee_id_dynamic_label_example",
            has_label("as_id", 345),
        )
    )
