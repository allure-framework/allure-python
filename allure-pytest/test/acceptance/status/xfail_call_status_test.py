from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_xfail(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.xfail()
    ... def test_xfail_example():
    ...     assert False

    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_xfail_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("XFAIL"),
                                                 with_message_contains("AssertionError"),
                                                 with_trace_contains("def test_xfail_example():")
                                                 )
                              )
                )


def test_xfail_with_reason_raise_mentioned_exception(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError, reason='Some reason')
    ... def test_xfail_with_reason_raise_mentioned_exception_example():
    ...     assert False

    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_xfail_with_reason_raise_mentioned_exception_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("XFAIL Some reason"),
                                                 with_message_contains("AssertionError"),
                                                 with_trace_contains(
                                                     "def test_xfail_with_reason_raise_mentioned_exception_example():")
                                                 )
                              )
                )


def test_xfail_raise_not_mentioned_exception(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError)
    ... def test_xfail_raise_not_mentioned_exception_example():
    ...     raise ZeroDivisionError
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_xfail_raise_not_mentioned_exception_example",
                              with_status("broken"),
                              has_status_details(with_message_contains("ZeroDivisionError"),
                                                 with_trace_contains(
                                                     "def test_xfail_raise_not_mentioned_exception_example():")
                                                 )
                              )
                )


def test_xfail_do_not_raise_mentioned_exception(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError)
    ... def test_xfail_do_not_raise_mentioned_exception_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_xfail_do_not_raise_mentioned_exception_example",
                              with_status("passed"),
                              has_status_details(with_message_contains("XPASS"),
                                                 )
                              )
                )


def test_xfail_with_reason_do_not_raise_mentioned_exception(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(raises=AssertionError, reason="Some reason")
    ... def test_xfail_with_reason_do_not_raise_mentioned_exception_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_xfail_with_reason_do_not_raise_mentioned_exception_example",
                              with_status("passed"),
                              has_status_details(with_message_contains("XPASS Some reason"),
                                                 )
                              )
                )
