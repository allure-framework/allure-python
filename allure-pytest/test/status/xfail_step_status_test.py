import pytest
import allure


@pytest.mark.xfail()
def test_xfail_step_failure():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_step_failure',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("AssertionError"),
    ...                                              with_trace_contains("def test_xfail_step_failure():")
    ...                           ),
    ...                           has_step('Step',
    ...                                    with_status('failed'),
    ...                                    has_status_details(with_message_contains("AssertionError"),
    ...                                                       with_trace_contains("test_xfail_step_failure")
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with allure.step('Step'):
        assert False
