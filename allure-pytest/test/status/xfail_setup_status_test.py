import pytest


@pytest.mark.xfail(run=False)
def test_xfail_with_run_false():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_with_run_false',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Failed: [NOTRUN]")),
    ...             )
    ... )
    """
    pass


@pytest.mark.xfail(run=False, reason='Some reason')
def test_xfail_with_run_false_and_with_reason():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_with_run_false_and_with_reason',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Failed: [NOTRUN] Some reason"))
    ...             )
    ... )
    """
    pass


@pytest.fixture
def broken_fixture():
    raise NotImplementedError


@pytest.mark.xfail()
def test_xfail_fixture(broken_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_fixture',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("NotImplementedError"),
    ...                                              with_trace_contains("def broken_fixture():")
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_before('broken_fixture',
    ...                                                    with_status('broken'),
    ...                                                    has_status_details(with_message_contains("NotImplementedError"),
    ...                                                                       with_trace_contains("broken_fixture")
    ...                                                    ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass
