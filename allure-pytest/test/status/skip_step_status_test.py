import pytest
import allure


def test_skip_in_step():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip_in_step',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Skipped: <Skipped instance>")),
    ...                           has_step('Step',
    ...                                    with_status('skipped'),
    ...                                    has_status_details(with_message_contains("Skipped: <Skipped instance>"),
    ...                                                       with_trace_contains("test_skip_in_step")
    ...                                    )
    ...                            )
    ...             )
    ... )
    """
    with allure.step('Step'):
        pytest.skip()
