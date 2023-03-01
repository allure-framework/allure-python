import pytest
from hamcrest import assert_that, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@pytest.fixture
def flakes_runner(allure_pytest_runner: AllurePytestRunner):
    allure_pytest_runner.enable_plugins("flakes")
    yield allure_pytest_runner


@allure.issue("352")
def test_pytest_flakes(flakes_runner: AllurePytestRunner):
    """
    >>> from os.path import *
    >>> def test_pytest_flakes_example():
    ...     assert True
    """

    output = flakes_runner.run_docstring("--flakes")

    assert_that(output, all_of(
        has_test_case(
            "flake-8",
            with_status("broken")
        ),
        has_test_case(
            "test_pytest_flakes_example",
            with_status("passed")
        )
    ))
