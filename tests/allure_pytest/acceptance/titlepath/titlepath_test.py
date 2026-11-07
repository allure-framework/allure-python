import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.label import has_package
from allure_commons_test.label import has_suite
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_full_name
from allure_commons_test.result import has_title_path


@pytest.mark.parametrize(["path", "path_segments"], [
    pytest.param("foo_test.py", ["foo_test.py"], id="root"),
    pytest.param("foo/bar_test.py", ["foo", "bar_test.py"], id="dir"),
    pytest.param("foo/bar/baz_test.py", ["foo", "bar", "baz_test.py"], id="subdir"),
])
def test_function_title_path(allure_pytest_runner: AllurePytestRunner, path, path_segments):
    """
    >>> def test_bar():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename=path)

    assert_that(
        allure_results,
        has_test_case(
            "test_bar",
            has_title_path(*path_segments),
        )
    )


@pytest.mark.parametrize(["path", "path_segments"], [
    pytest.param("foo_test.py", ["foo_test.py"], id="root"),
    pytest.param("foo/bar_test.py", ["foo", "bar_test.py"], id="dir"),
    pytest.param("foo/bar/baz_test.py", ["foo", "bar", "baz_test.py"], id="subdir"),
])
def test_method_title_path(allure_pytest_runner: AllurePytestRunner, path, path_segments):
    """
    >>> class TestBar:
    ...     def test_baz(self):
    ...         pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename=path)

    assert_that(
        allure_results,
        has_test_case(
            "test_baz",
            has_title_path(*path_segments, "TestBar"),
        )
    )


@pytest.mark.parametrize(["path", "path_segments"], [
    pytest.param("foo_test.py", ["foo_test.py"], id="root"),
    pytest.param("foo/bar_test.py", ["foo", "bar_test.py"], id="dir"),
    pytest.param("foo/bar/baz_test.py", ["foo", "bar", "baz_test.py"], id="subdir"),
])
def test_nested_class_method_title_path(allure_pytest_runner: AllurePytestRunner, path, path_segments):
    """
    >>> class TestBar:
    ...     class TestBaz:
    ...         def test_qux(self):
    ...             pass
    """

    allure_results = allure_pytest_runner.run_docstring(filename=path)

    assert_that(
        allure_results,
        has_test_case(
            "test_qux",
            has_title_path(*path_segments, "TestBar", "TestBaz"),
        )
    )


def test_file_path_with_double_colon(
    allure_pytest_runner: AllurePytestRunner,
):
    allure_pytest_runner.pytester.makepyfile(**{
        "test_module::part.py": """
        def test_fn():
            pass
        """
    })

    allure_results = allure_pytest_runner.run_pytest()

    assert_that(
        allure_results,
        has_test_case(
            "test_fn",
            has_full_name("test_module::part#test_fn"),
            has_title_path("test_module::part.py"),
            has_package("test_module::part"),
            has_suite("test_module::part"),
        )
    )
