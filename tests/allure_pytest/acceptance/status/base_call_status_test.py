from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_passed(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_passed_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_passed_example",
            with_status("passed")
        )
    )


def test_failed(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_failed_example():
    ...     assert False
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_failed_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("AssertionError"),
                with_trace_contains("def test_failed_example():")
            )
        )
    )


def test_broken(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_broken_example():
    ...     raise IndentationError()
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_broken_example",
            with_status("broken"),
            has_status_details(
                with_message_contains("IndentationError"),
                with_trace_contains("def test_broken_example():")
            )
        )
    )


def test_call_pytest_fail(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> def test_call_pytest_fail_example():
    ...     pytest.fail()
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_call_pytest_fail_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("Failed"),
                with_trace_contains("def test_call_pytest_fail_example():")
            )
        )
    )


def test_call_pytest_fail_with_reason(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> def test_call_pytest_fail_with_reason_example():
    ...     pytest.fail("Fail message")
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_call_pytest_fail_with_reason_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("Fail message"),
                with_trace_contains("def test_call_pytest_fail_with_reason_example():")
            )
        )
    )
