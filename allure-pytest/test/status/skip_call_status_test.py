import pytest


def test_skip():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Skipped: <Skipped instance>"))
    ...             )
    ... )
    """
    pytest.skip()


def test_skip_with_reason():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip_with_reason',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Skipped: Skip reason"))
    ...             )
    ... )
    """
    pytest.skip('Skip reason')


@pytest.mark.skip(reason='Skip reason')
def test_skip_decorator_and_reason():
    """
     >>> allure_report = getfixture('allure_report')
     >>> assert_that(allure_report,
     ...             has_test_case('test_skip_decorator_and_reason',
     ...                            with_status('skipped'),
     ...                            has_status_details(with_message_contains("Skipped: Skip reason"))
     ...             )
     ... )
     """
    pass


@pytest.mark.skipif(True, reason='Skip reason')
def test_skipif_true():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skipif_true',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Skipped: Skip reason"))
    ...             )
    ... )
    """
    pass


@pytest.mark.skipif(False, reason='Skip reason')
def test_skipif_false():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skipif_false',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass
