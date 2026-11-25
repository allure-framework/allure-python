from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_full_name, with_status


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


@allure.feature("Integration")
def test_pytest_doctest_text_filename_preserves_brackets(allure_pytest_runner: AllurePytestRunner):
    """
    >>> assert True
    """

    output = allure_pytest_runner.run_pytest(
        ("spec[foo].txt", ">>> assert True\n"),
        cli_args=("--doctest-glob=*.txt",),
    )

    assert_that(output, has_test_case(
        "spec[foo]#spec[foo].txt",
        has_full_name("spec[foo]#spec[foo].txt"),
        with_status("passed"),
    ))
