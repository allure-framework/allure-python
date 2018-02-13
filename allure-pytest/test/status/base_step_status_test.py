import pytest


def test_broken_step():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_broken_step',
    ...                           with_status('broken'),
    ...                           has_status_details(with_message_contains("ZeroDivisionError"),
    ...                                              with_trace_contains("def test_broken_step():")
    ...                           ),
    ...                           has_step('Step',
    ...                                    with_status('broken'),
    ...                                    has_status_details(with_message_contains("ZeroDivisionError"),
    ...                                                       with_trace_contains("test_broken_step")
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with pytest.allure.step('Step'):
        raise ZeroDivisionError


def test_pytest_fail_in_step():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_fail_in_step',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                              with_trace_contains("def test_pytest_fail_in_step():")
    ...                           ),
    ...                           has_step('Step',
    ...                                    with_status('failed'),
    ...                                    has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                                       with_trace_contains("test_pytest_fail_in_step")
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with pytest.allure.step('Step'):
        pytest.fail()
