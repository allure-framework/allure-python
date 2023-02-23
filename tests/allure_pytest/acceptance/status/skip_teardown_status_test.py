from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_after


def test_skip_finalizer_fixture(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def skip_finalizer_fixture(request):
    ...     def fixture_finalizer():
    ...         pytest.skip()
    ...     request.addfinalizer(fixture_finalizer)

    >>> def test_skip_finalizer_fixture_example(skip_finalizer_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_skip_finalizer_fixture_example",
            with_status("passed"),
            has_container(
                allure_results,
                has_after(
                    "skip_finalizer_fixture::fixture_finalizer",
                    with_status("skipped"),
                    has_status_details(
                        with_message_contains("Skipped"),
                        with_trace_contains("fixture_finalizer")
                    )
                )
            )
        )
    )
