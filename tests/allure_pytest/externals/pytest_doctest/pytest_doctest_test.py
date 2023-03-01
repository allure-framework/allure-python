from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@allure.feature("Integration")
def test_pytest_doctest(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def some_func():
    ...     '''
    ...     >>> some_func()
    ...     True
    ...     '''
    ...     return True

    """

    output = allure_pytest_runner.run_docstring("--doctest-modules")

    assert_that(output, has_test_case(
        "test_pytest_doctest.some_func",
        with_status("passed")
    ))


@allure.feature("Integration")
def test_pytest_doctest_failed(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def some_func():
    ...     '''
    ...     >>> some_func()
    ...     True
    ...     '''
    ...     return not True

    """

    output = allure_pytest_runner.run_docstring("--doctest-modules")

    assert_that(output, has_test_case(
        "test_pytest_doctest_failed.some_func",
        with_status("failed")
    ))


@allure.feature("Integration")
def test_pytest_doctest_broken(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def some_func():
    ...     '''
    ...     >>> raise ValueError()
    ...     '''
    """

    output = allure_pytest_runner.run_docstring("--doctest-modules")

    assert_that(output, has_test_case(
        "test_pytest_doctest_broken.some_func",
        with_status("broken")
    ))
