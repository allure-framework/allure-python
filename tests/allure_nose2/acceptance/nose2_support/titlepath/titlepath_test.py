import pytest
from hamcrest import assert_that
from tests.allure_nose2.nose2_runner import AllureNose2Runner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title_path


@pytest.mark.parametrize(["module", "path_segments"], [
    pytest.param("foo", ["foo"], id="root"),
    pytest.param("foo.bar", ["foo", "bar"], id="level1"),
    pytest.param("foo.bar.baz", ["foo", "bar", "baz"], id="level2"),
])
def test_function_title_path(nose2_runner: AllureNose2Runner, module, path_segments):
    """
    >>> def test_qux():
    ...     pass
    """

    allure_results = nose2_runner.run_docstring(module_name=module)

    assert_that(
        allure_results,
        has_test_case(
            "test_qux",
            has_title_path(*path_segments),
        )
    )


@pytest.mark.parametrize(["module", "path_segments"], [
    pytest.param("foo", ["foo"], id="root"),
    pytest.param("foo.bar", ["foo", "bar"], id="level1"),
    pytest.param("foo.bar.baz", ["foo", "bar", "baz"], id="level2"),
])
def test_method_title_path(nose2_runner: AllureNose2Runner, module, path_segments):
    """
    >>> from unittest import TestCase
    >>> class TestQux(TestCase):
    ...     def test_quux(self):
    ...         pass
    """

    allure_results = nose2_runner.run_docstring(module_name=module)

    assert_that(
        allure_results,
        has_test_case(
            "test_quux",
            has_title_path(*path_segments, "TestQux"),
        )
    )


def test_params_ignored(nose2_runner: AllureNose2Runner):
    """
    >>> from nose2.tools import params
    >>> @params("a.b:c")
    ... def test_bar(v):
    ...     pass
    """

    allure_results = nose2_runner.run_docstring(module_name="foo")

    assert_that(
        allure_results,
        has_test_case(
            "test_bar",
            has_title_path("foo"),
        )
    )
