import pytest


@pytest.fixture
def failed_fixture():
    assert False


def test_failed_fixture(failed_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_failed_fixture',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("AssertionError"),
    ...                                              with_trace_contains("def failed_fixture():")
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_before('failed_fixture',
    ...                                                    with_status('failed'),
    ...                                                    has_status_details(with_message_contains("AssertionError"),
    ...                                                                       with_trace_contains("failed_fixture")
    ...                                                    ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.fixture
def broken_fixture():
    raise IndexError


def test_broken_fixture(broken_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_broken_fixture',
    ...                           with_status('broken'),
    ...                           has_status_details(with_message_contains("IndexError"),
    ...                                              with_trace_contains("def broken_fixture():")
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_before('broken_fixture',
    ...                                                    with_status('broken'),
    ...                                                    has_status_details(with_message_contains("IndexError"),
    ...                                                                       with_trace_contains("broken_fixture")
    ...                                                    ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.fixture
def skip_fixture():
    pytest.skip()


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


@pytest.fixture
def pytest_fail_fixture():
    pytest.fail()


def test_pytest_fail_fixture(pytest_fail_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_fail_fixture',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                              with_trace_contains("def pytest_fail_fixture():")
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_before('pytest_fail_fixture',
    ...                                                    with_status('failed'),
    ...                                                    has_status_details(with_message_contains("Failed: <Failed instance>"),
    ...                                                                       with_trace_contains("pytest_fail_fixture")
    ...                                                    ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass


@pytest.fixture
def pytest_fail_with_reason_fixture():
    pytest.fail("Fail message")


def test_pytest_fail_with_reason_fixture(pytest_fail_with_reason_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_fail_with_reason_fixture',
    ...                           with_status('failed'),
    ...                           has_status_details(with_message_contains("Fail message"),
    ...                                              with_trace_contains("def pytest_fail_with_reason_fixture():")
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_before('pytest_fail_with_reason_fixture',
    ...                                                    with_status('failed'),
    ...                                                    has_status_details(with_message_contains("Fail message"),
    ...                                                                       with_trace_contains("pytest_fail_with_reason_fixture")
    ...                                                    ),
    ...                                         ),
    ...                           )
    ...             )
    ... )
    """
    pass


