from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before


@allure.feature("Fixture")
def test_skip_fixture(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.fixture
    ... def skip_fixture():
    ...     pytest.skip()

    >>> @pytest.mark.xfail()
    ... def test_skip_fixture_example(skip_fixture):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_skip_fixture_example",
            with_status("skipped"),
            has_status_details(
                with_message_contains("Skipped")
            ),
            has_container(
                allure_results,
                has_before(
                    "skip_fixture",
                    with_status("skipped"),
                    has_status_details(
                        with_message_contains("Skipped"),
                        with_trace_contains("skip_fixture")
                    )
                )
            )
        )
    )
