import pytest


@pytest.fixture
def failed_finalizer_fixture(request):
    def fixture_finalizer():
        assert False
    request.addfinalizer(fixture_finalizer)


@pytest.mark.xfail()
def test_xfail_failed_finalizer_fixture(failed_finalizer_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_xfail_failed_finalizer_fixture',
    ...                           with_status('passed'),
    ...                           has_status_details(with_message_contains("XPASS")),
    ...                           has_container(allure_report,
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='failed_finalizer_fixture',
    ...                                                               finalizer='fixture_finalizer'),
    ...                                                   with_status('failed'),
    ...                                                   has_status_details(with_message_contains("AssertionError"),
    ...                                                                      with_trace_contains("fixture_finalizer")
    ...                                                   ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass
