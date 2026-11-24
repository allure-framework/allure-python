import pytest


@pytest.mark.parametrize("entry", [{"id": 12}, {"id": "missing", "selector": "exclusion.test_excluded"}])
def test_excluded_functions(nose2_runner, entry):
    """
    >>> import allure
    >>> from nose2.tools import params
    >>> @allure.id("12")
    ... @params("one", "two")
    ... def test_excluded(value):
    ...     raise AssertionError("excluded body ran")
    >>> def test_active():
    ...     pass
    """
    results = nose2_runner.run_docstring(module_name="exclusion", testplan={"excludedTests": [entry]})

    excluded = [result for result in results.test_cases if result["fullName"] == "exclusion.test_excluded"]
    assert len(results.test_cases) == 3
    assert len(excluded) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] for result in excluded)
    assert next(result for result in results.test_cases if result["name"] == "test_active")["status"] == "passed"


@pytest.mark.parametrize("entry", [{"id": "34"}, {"selector": "exclusion.TestExcluded.test_excluded"}])
def test_excluded_methods(nose2_runner, entry):
    """
    >>> import allure
    >>> from unittest import TestCase
    >>> @allure.id(34)
    ... class TestExcluded(TestCase):
    ...     def setUp(self):
    ...         raise AssertionError("excluded setup ran")
    ...     def test_excluded(self):
    ...         raise AssertionError("excluded body ran")
    """
    results = nose2_runner.run_docstring(module_name="exclusion", testplan={"tests": [], "excludedTests": [entry]})

    assert len(results.test_cases) == 1
    assert results.test_cases[0]["status"] == "skipped"
    assert results.test_cases[0]["statusDetails"]["muted"] is True


def test_excluded_parameterized_methods(nose2_runner):
    """
    >>> import allure
    >>> from nose2.tools import params
    >>> from unittest import TestCase
    >>> class TestExcluded(TestCase):
    ...     @allure.id("56")
    ...     @params("one", "two")
    ...     def test_excluded(self, value):
    ...         raise AssertionError("excluded body ran")
    ...     def test_active(self):
    ...         pass
    """
    results = nose2_runner.run_docstring(module_name="exclusion", testplan={"excludedTests": [{"id": 56}]})

    excluded = [result for result in results.test_cases if result["name"].startswith("test_excluded")]
    assert len(excluded) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] for result in excluded)
    assert next(result for result in results.test_cases if result["name"] == "test_active")["status"] == "passed"
