import pytest


def test_passed():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_passed',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass


def test_failed():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_failed',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("AssertionError"),
    ...                                              with_trace_contains("def test_failed():")
    ...                           )
    ...             )
    ... )
    """
    assert False


def test_broken():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_broken',
    ...                           with_status('broken'),
    ...                           has_status_details(with_message_contains("IndentationError"),
    ...                                              with_trace_contains("def test_broken():")
    ...                           )
    ...             )
    ... )
    """
    raise IndentationError()


def test_call_pytest_fail():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_call_pytest_fail',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                              with_trace_contains("def test_call_pytest_fail():")
    ...                           )
    ...             )
    ... )
    """
    pytest.fail()


def test_call_pytest_fail_with_reason():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_call_pytest_fail_with_reason',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("Fail message"),
    ...                                              with_trace_contains("def test_call_pytest_fail():")
    ...                           )
    ...             )
    ... )
    """
    pytest.fail("Fail message")

