from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_history_id


def test_history_id(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_history_id_example():
    ...     assert True
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_history_id_example",
            has_history_id()
        )
    )


def test_history_id_for_skipped(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.skip
    ... def test_history_id_for_skipped_example():
    ...     assert True
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_history_id_for_skipped_example",
            has_history_id()
        )
    )
