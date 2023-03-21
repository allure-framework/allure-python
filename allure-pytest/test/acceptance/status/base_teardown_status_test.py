from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_after


def test_failed_finalizer_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def failed_finalizer_fixture(request):
    ...     def fixture_finalizer():
    ...         assert False
    ...     request.addfinalizer(fixture_finalizer)
    ...
    ... def test_failed_finalizer_fixture_example(failed_finalizer_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_failed_finalizer_fixture_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("AssertionError"),
                                                 with_trace_contains("def fixture_finalizer():")
                                                 ),
                              has_container(executed_docstring_source.allure_report,
                                            has_after("{fixture}::{finalizer}".format(
                                                fixture="failed_finalizer_fixture",
                                                finalizer="fixture_finalizer"),
                                                with_status("failed"),
                                                has_status_details(with_message_contains("AssertionError"),
                                                                   with_trace_contains("fixture_finalizer")
                                                                   ),
                                            ),
                                            )
                              )
                )


def test_pytest_failed_finalizer_fixture(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def pytest_failed_finalizer_fixture(request):
    ...     def fixture_finalizer():
    ...         pytest.fail()
    ...     request.addfinalizer(fixture_finalizer)

    >>> def test_pytest_failed_finalizer_fixture_example(pytest_failed_finalizer_fixture):
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_pytest_failed_finalizer_fixture_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("Failed"),
                                                 with_trace_contains("def fixture_finalizer():")
                                                 ),
                              has_container(executed_docstring_source.allure_report,
                                            has_after("{fixture}::{finalizer}".format(
                                                fixture="pytest_failed_finalizer_fixture",
                                                finalizer="fixture_finalizer"),
                                                with_status("failed"),
                                                has_status_details(with_message_contains("Failed"),
                                                                   with_trace_contains("fixture_finalizer")
                                                                   ),
                                            ),
                                            )
                              )
                )
