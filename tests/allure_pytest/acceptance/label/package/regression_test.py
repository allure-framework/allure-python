import textwrap
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_package


def test_path_with_dots_test(allure_pytest_runner: AllurePytestRunner):
    package_path = allure_pytest_runner.pytester.mkpydir("path.with.dots")
    package_path.joinpath("test_path.py").write_text(
        textwrap.dedent(
            """
            def test_path_with_dots_test_example():
                pass
            """
        )
    )

    allure_results = allure_pytest_runner.run_pytest()

    assert_that(
        allure_results,
        has_test_case(
            "test_path_with_dots_test_example",
            has_package("path.with.dots.test_path")
        )
    )


def test_with_no_package(allure_pytest_runner: AllurePytestRunner):
    """
    >>> def test_package_less(request):
    ...     pass
    """

    allure_pytest_runner.pytester.makeini("""[pytest]""")

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_package_less",
            has_package("test_with_no_package")
        )
    )
