from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


def test_failed_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def failed_fixture():
    ...     assert False

    >>> def test_failed_fixture_example(failed_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_failed_fixture_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("AssertionError"),
                                                 with_trace_contains("def failed_fixture():")
                                                 ),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("failed_fixture",
                                                       with_status("failed"),
                                                       has_status_details(with_message_contains("AssertionError"),
                                                                          with_trace_contains("failed_fixture")
                                                                          ),
                                                       ),
                                            )
                              )
                )


def test_broken_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def broken_fixture():
    ...     raise IndexError

    >>> def test_broken_fixture_example(broken_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_broken_fixture_example",
                              with_status("broken"),
                              has_status_details(with_message_contains("IndexError"),
                                                 with_trace_contains("def broken_fixture():")
                                                 ),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("broken_fixture",
                                                       with_status("broken"),
                                                       has_status_details(with_message_contains("IndexError"),
                                                                          with_trace_contains("broken_fixture")
                                                                          ),
                                                       ),
                                            )
                              )
                )


def test_skip_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def skip_fixture():
    ...     pytest.skip()

    >>> def test_skip_fixture_example(skip_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skip_fixture_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("Skipped: <Skipped instance>")),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("skip_fixture",
                                                       with_status("skipped"),
                                                       has_status_details(
                                                           with_message_contains("Skipped: <Skipped instance>"),
                                                           with_trace_contains("skip_fixture")
                                                       ),
                                                       ),
                                            )
                              )
                )


def test_pytest_fail_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def pytest_fail_fixture():
    ...     pytest.fail()

    >>> def test_pytest_fail_fixture_example(pytest_fail_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_pytest_fail_fixture_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("Failed: <Failed instance>"),
                                                 with_trace_contains("def pytest_fail_fixture():")
                                                 ),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("pytest_fail_fixture",
                                                       with_status("failed"),
                                                       has_status_details(
                                                           with_message_contains("Failed: <Failed instance>"),
                                                           with_trace_contains("pytest_fail_fixture")
                                                       ),
                                                       ),
                                            )
                              )
                )


def test_pytest_fail_with_reason_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def pytest_fail_with_reason_fixture():
    ...     pytest.fail("Fail message")

    >>> def test_pytest_fail_with_reason_fixture_example(pytest_fail_with_reason_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_pytest_fail_with_reason_fixture_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("Fail message"),
                                                 with_trace_contains("def pytest_fail_with_reason_fixture():")
                                                 ),
                              has_container(executed_docstring_source.allure_report,
                                            has_before("pytest_fail_with_reason_fixture",
                                                       with_status("failed"),
                                                       has_status_details(with_message_contains("Fail message"),
                                                                          with_trace_contains(
                                                                              "pytest_fail_with_reason_fixture")
                                                                          ),
                                                       ),
                                            )
                              )
                )
