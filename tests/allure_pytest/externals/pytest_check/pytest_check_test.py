import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status, with_message_contains, has_status_details


@pytest.fixture
def check_runner(allure_pytest_runner: AllurePytestRunner):
    allure_pytest_runner.enable_plugins("check")
    yield allure_pytest_runner


@allure.issue("376")
@allure.feature("Integration")
def test_pytest_check(check_runner: AllurePytestRunner):
    """
    >>> import pytest_check as check
    >>> def test_pytest_check_example():
    ...     check.equal(1, 2, msg="First failure")
    ...     check.equal(1, 2, msg="Second failure")
    """

    output = check_runner.run_docstring()

    assert_that(
        output,
        has_test_case(
            "test_pytest_check_example",
            with_status("failed"),
            has_status_details(
                with_message_contains("First failure"),
                with_message_contains("Second failure")
            )
        )
    )
