import threading
import pytest

lord_of_the_flies = threading.local()


@pytest.mark.flaky(reruns=5)
def test_rerunfialures_failed_to_passed():
    """
    >>> allure_report = getfixture('allure_report')

    >>> assert_that(allure_report,
    ...             has_test_case('test_rerunfialures_failed_to_passed',
    ...                           with_status('failed')
    ...             )
    ... )

    >>> assert_that(allure_report,
    ...             has_test_case('test_rerunfialures_failed_to_passed',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    saved = getattr(lord_of_the_flies, 'good', False)
    lord_of_the_flies.good = saved or 'maybe next time'
    assert saved
