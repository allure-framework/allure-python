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


def test_pytest_fail_in_nested_step_with_soft_check(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> from pytest_check import check as soft_check

    >>> def test_pytest_fail_in_nested_step_with_soft_check():
    ...     with allure.step("Parent step"):
    ...         with soft_check, allure.step("Child failed step"):
    ...             assert False
    ...         with soft_check, allure.step("Child passed step"):
    ...             assert True
    """
    from pytest_check import check_log

    allure_results = allure_pytest_runner.run_docstring()
    # Prevent failed soft check checks from triggering an 'assert False'.
    check_log.clear_failures()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_fail_in_nested_step_with_soft_check",
            with_status("failed"),
            has_step(
                "Parent step",
                with_status("failed"),
                has_step(
                    "Child failed step",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("AssertionError: assert False"),
                        with_trace_contains("test_pytest_fail_in_nested_step_with_soft_check")
                    )
                ),
                has_step(
                    "Child passed step",
                    with_status("passed")
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
