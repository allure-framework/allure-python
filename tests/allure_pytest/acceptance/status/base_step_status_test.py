from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_broken_step(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_broken_step_example():
    ...     with allure.step("Step"):
    ...         raise ZeroDivisionError
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_broken_step_example",
            with_status("broken"),
            has_status_details(
                with_message_contains("ZeroDivisionError"),
                with_trace_contains("def test_broken_step_example():")
            ),
            has_step(
                "Step",
                with_status("broken"),
                has_status_details(
                    with_message_contains("ZeroDivisionError"),
                    with_trace_contains("test_broken_step_example")
                )
            )
        )
    )


def test_pytest_fail_in_step(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest
    >>> import allure

    >>> def test_pytest_fail_in_step_example():
    ...     with allure.step("Step"):
    ...         pytest.fail()
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_fail_in_step_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("Failed"),
                with_trace_contains("def test_pytest_fail_in_step_example():")
            ),
            has_step(
                "Step",
                with_status("failed"),
                has_status_details(
                    with_message_contains("Failed"),
                    with_trace_contains("test_pytest_fail_in_step_example")
                )
            )
        )
    )


def test_pytest_bytes_data_in_assert(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure

    >>> def test_pytest_bytes_data_in_assert_example():
    ...     with allure.step("Step"):
    ...         assert "0\\x82" == 1
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_bytes_data_in_assert_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("AssertionError: assert \'0\\x82\' == 1"),
                with_trace_contains("def test_pytest_bytes_data_in_assert_example():")
            ),
            has_step(
                "Step",
                with_status("failed"),
                has_status_details(
                    with_message_contains("AssertionError: assert \'0\\x82\' == 1"),
                    with_trace_contains("test_pytest_bytes_data_in_assert_example")
                )
            )
        )
    )
