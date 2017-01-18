import pytest


XFAIL_REASON = "THIS IS EXPECTED FAIL"
SKIP_REASON = "SKIPPED TEST"


def test_passed():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_passed', with_status('passed')))
    """
    pass


def test_failed():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_failed', with_status('failed')))
    """
    assert False


@pytest.mark.xfail(reason=XFAIL_REASON)
def test_xfailed():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_xfailed',
    ...                                          with_status('canceled'),
    ...                                          has_status_details(with_status_message(XFAIL_REASON))))
    """
    assert False


@pytest.mark.xfail(raises=RuntimeError)
def test_xfailed_not_mentioned_exception():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_passed', with_status('passed')))
    """
    assert False


@pytest.mark.xfail(reason=XFAIL_REASON)
def test_xfailed_but_passed():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_xfailed_but_passed',
    ...                                          with_status('passed'),
    ...                                          has_status_details(with_status_message(XFAIL_REASON))))
    """
    pass


def test_skip_in_test():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, test_skip_in_test, with_status('canceled'))
    """
    pytest.skip()


def test_skip_with_reason_in_test():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_skip_with_reason_in_test',
    ...                                          with_status('canceled'),
    ...                                          has_status_details(with_status_message(SKIP_REASON))))
    """
    pytest.skip(SKIP_REASON)


@pytest.mark.skip(reason=SKIP_REASON)
def test_skip_with_decorator_and_reason():
    """
     >>> allure_report = getfixture('allure_report')
     >>> assert_that(allure_report, has_test_case('test_skip_with_decorator_and_reason',
     ...                                          with_status('canceled'),
     ...                                          has_status_details(with_status_message(SKIP_REASON))))
     """
    pass


@pytest.mark.skipif(True, reason=SKIP_REASON)
def test_skipif_true():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_skipif_true',
    ...                                          with_status('canceled'),
    ...                                          has_status_details(with_status_message(SKIP_REASON))))
    """
    pass


@pytest.mark.skipif(False, reason=SKIP_REASON)
def test_skipif_false():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report, has_test_case('test_skipif_false', with_status('passed')))
    """
    pass
