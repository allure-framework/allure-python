import pytest


@pytest.fixture
def skip_finalizer_fixture(request):
    def fixture_finalizer():
        pytest.skip()
    request.addfinalizer(fixture_finalizer)


def test_skip_finalizer_fixture(skip_finalizer_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_skip_finalizer_fixture',
    ...                           with_status('passed'),
    ...                           has_container(allure_report,
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='skip_finalizer_fixture',
    ...                                                               finalizer='fixture_finalizer'),
    ...                                                   with_status('skipped'),
    ...                                                   has_status_details(with_message_contains("Skipped: <Skipped instance>"),
    ...                                                                      with_trace_contains("fixture_finalizer")
    ...                                                   ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass
