import pytest


@pytest.mark.xfail()
def test_xfail():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("AssertionError"),
    ...                                              with_trace_contains("def test_xfail():")
    ...                           )
    ...             )
    ... )
    """
    assert False


@pytest.mark.xfail(raises=AssertionError)
def test_xfail_raise_mentioned_exception():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_raise_mentioned_exception',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("AssertionError"),
    ...                                              with_trace_contains("def test_xfail_raise_mentioned_exception():")
    ...                           )
    ...             )
    ... )
    """
    assert False


@pytest.mark.xfail(raises=AssertionError)
def test_xfail_raise_not_mentioned_exception():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_raise_not_mentioned_exception',
    ...                           with_status('broken'),
    ...                           has_status_details(with_message_contains("ZeroDivisionError"),
    ...                                              with_trace_contains("def test_xfail_raise_not_mentioned_exception():")
    ...                           )
    ...             )
    ... )
    """
    raise ZeroDivisionError


@pytest.mark.xfail(raises=AssertionError)
def test_xfail_do_not_raise_mentioned_exception():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_do_not_raise_mentioned_exception',
    ...                           with_status('passed'),
    ...                           has_status_details(with_message_contains("XPASS"),
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.mark.xfail(raises=AssertionError, reason='Some reason')
def test_xfail_with_reason_do_not_raise_mentioned_exception():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_with_reason_do_not_raise_mentioned_exception',
    ...                           with_status('passed'),
    ...                           has_status_details(with_message_contains("XPASS Some reason"),
    ...                           )
    ...             )
    ... )
    """
    pass



