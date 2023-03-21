from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_passed(executed_docstring_source):
    """
    >>> def test_passed_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_passed_example",
                              with_status("passed")
                              )
                )


def test_failed(executed_docstring_source):
    """
    >>> def test_failed_example():
    ...     assert False
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_failed_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("AssertionError"),
                                                 with_trace_contains("def test_failed_example():")
                                                 )
                              )
                )


def test_broken(executed_docstring_source):
    """
    >>> def test_broken_example():
    ...     raise IndentationError()
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_broken_example",
                              with_status("broken"),
                              has_status_details(with_message_contains("IndentationError"),
                                                 with_trace_contains("def test_broken_example():")
                                                 )
                              )
                )


def test_call_pytest_fail(executed_docstring_source):
    """
    >>> import pytest

    >>> def test_call_pytest_fail_example():
    ...     pytest.fail()
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_call_pytest_fail_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("Failed"),
                                                 with_trace_contains("def test_call_pytest_fail_example():")
                                                 )
                              )
                )


def test_call_pytest_fail_with_reason(executed_docstring_source):
    """
    >>> import pytest

    >>> def test_call_pytest_fail_with_reason_example():
    ...     pytest.fail("Fail message")
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_call_pytest_fail_with_reason_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("Fail message"),
                                                 with_trace_contains("def test_call_pytest_fail_with_reason_example():")
                                                 )
                              )

                )
