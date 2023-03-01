from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_after


def test_xfail_failed_finalizer_fixture(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def failed_finalizer_fixture(request):
    ...     def fixture_finalizer():
    ...         assert False
    ...     request.addfinalizer(fixture_finalizer)

    >>> @pytest.mark.xfail()
    ... def test_xfail_failed_finalizer_fixture_example(failed_finalizer_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_failed_finalizer_fixture_example",
            with_status("passed"),
            has_status_details(
                with_message_contains("XPASS")
            ),
            has_container(
                allure_results,
                has_after(
                    "failed_finalizer_fixture::fixture_finalizer",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("AssertionError"),
                        with_trace_contains("fixture_finalizer")
                    )
                )
            )
        )
    )
