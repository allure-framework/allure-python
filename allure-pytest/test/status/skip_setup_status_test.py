import pytest


@pytest.fixture
def skip_fixture():
    pytest.skip()


@pytest.mark.xfail()
def test_skip_fixture(skip_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip_fixture',
    ...                           with_status('skipped'),
    ...                           has_status_details(with_message_contains("Skipped: <Skipped instance>")),
    ...                           has_container(allure_report,
    ...                                         has_before('skip_fixture',
    ...                                                    with_status('skipped'),
    ...                                                    has_status_details(with_message_contains("Skipped: <Skipped instance>"),
    ...                                                                       with_trace_contains("skip_fixture")
    ...                                                    ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass

