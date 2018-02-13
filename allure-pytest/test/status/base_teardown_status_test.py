import pytest


@pytest.fixture
def failed_finalizer_fixture(request):
    def fixture_finalizer():
        assert False
    request.addfinalizer(fixture_finalizer)


def test_failed_finalizer_fixture(failed_finalizer_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_failed_finalizer_fixture',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("AssertionError"),
    ...                                              with_trace_contains("def fixture_finalizer():")
    ...                           ),
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


@pytest.fixture
def pytest_failed_finalizer_fixture(request):
    def fixture_finalizer():
        pytest.fail()
    request.addfinalizer(fixture_finalizer)


def test_pytest_failed_finalizer_fixture(pytest_failed_finalizer_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_failed_finalizer_fixture',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                              with_trace_contains("def fixture_finalizer():")
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='pytest_failed_finalizer_fixture',
    ...                                                               finalizer='fixture_finalizer'),
    ...                                                   with_status('failed'),
    ...                                                   has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                                                      with_trace_contains("fixture_finalizer")
    ...                                                   ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass