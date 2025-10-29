from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_package


def test_with_no_package(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_bar(request):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename="foo_test.py")

    assert_that(
        allure_results,
        has_test_case(
            "test_bar",
            has_package("foo_test")
        )
    )


def test_with_package(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_qux(request):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename="foo/bar/baz_test.py")

    assert_that(
        allure_results,
        has_test_case(
            "test_qux",
            has_package("foo.bar.baz_test"),
        )
    )
