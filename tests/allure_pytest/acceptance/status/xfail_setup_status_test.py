from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


def test_xfail_with_run_false(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(run=False)
    ... def test_xfail_with_run_false_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_with_run_false_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("Failed: [NOTRUN]")
            )
        )
    )


def test_xfail_with_run_false_and_with_reason(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(run=False, reason="Some reason")
    ... def test_xfail_with_run_false_and_with_reason_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_with_run_false_and_with_reason_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("Failed: [NOTRUN] Some reason")
            )
        )
    )


def test_xfail_fixture(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def broken_fixture():
    ...     raise NotImplementedError

    >>> @pytest.mark.xfail()
    ... def test_xfail_fixture_example(broken_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_xfail_fixture_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("NotImplementedError"),
                with_trace_contains("def broken_fixture():")
            ),
            has_container(
                allure_results,
                has_before(
                    "broken_fixture",
                    with_status("broken"),
                    has_status_details(
                        with_message_contains("NotImplementedError"),
                        with_trace_contains("broken_fixture")
                    ),
                ),
            )
        )
    )
