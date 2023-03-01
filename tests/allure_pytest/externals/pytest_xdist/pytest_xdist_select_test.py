import pytest
from hamcrest import assert_that, ends_with, has_entry
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_only_testcases


@pytest.fixture
def xdist_runner(allure_pytest_runner: AllurePytestRunner):
    allure_pytest_runner.in_memory = False
    allure_pytest_runner.enable_plugins("xdist")
    yield allure_pytest_runner


@allure.issue("292")
@allure.feature("Integration")
def test_xdist_and_select_test_by_bdd_label(xdist_runner: AllurePytestRunner):
    """
    >>> import pytest
    >>> import allure

    >>> @pytest.mark.foo
    ... def test_with_mark_foo():
    ...     print ("hello")

    >>> @allure.feature("boo")
    ... def test_with_feature_boo():
    ...     print ("hello")
    """

    output = xdist_runner.run_docstring("-v", "--allure-features=boo", "-n1")

    assert_that(output, has_only_testcases(
        has_entry(
            "fullName",
            ends_with("test_with_feature_boo")
        )
    ))
