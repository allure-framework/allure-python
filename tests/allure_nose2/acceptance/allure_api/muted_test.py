import pytest


@pytest.mark.parametrize("entry", [{"id": 12}, {"id": "missing", "selector": "muting.test_muted"}])
def test_muted_functions(nose2_runner, entry):
    """
    >>> import allure
    >>> from nose2.tools import params
    >>> @allure.id("12")
    ... @params("one", "two")
    ... def test_muted(value):
    ...     raise AssertionError("muted body ran")
    >>> def test_active():
    ...     pass
    """
    results = nose2_runner.run_docstring(module_name="muting", testplan={"mutedTests": [entry]})

    muted = [result for result in results.test_cases if result["fullName"] == "muting.test_muted"]
    assert len(results.test_cases) == 3
    assert len(muted) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] for result in muted)
    assert next(result for result in results.test_cases if result["name"] == "test_active")["status"] == "passed"


@pytest.mark.parametrize("entry", [{"id": "34"}, {"selector": "muting.TestMuted.test_muted"}])
def test_muted_methods(nose2_runner, entry):
    """
    >>> import allure
    >>> from unittest import TestCase
    >>> @allure.id(34)
    ... class TestMuted(TestCase):
    ...     def setUp(self):
    ...         raise AssertionError("muted setup ran")
    ...     def test_muted(self):
    ...         raise AssertionError("muted body ran")
    """
    results = nose2_runner.run_docstring(module_name="muting", testplan={"tests": [], "mutedTests": [entry]})

    assert len(results.test_cases) == 1
    assert results.test_cases[0]["status"] == "skipped"
    assert results.test_cases[0]["statusDetails"]["muted"] is True


def test_muted_parameterized_methods(nose2_runner):
    """
    >>> import allure
    >>> from nose2.tools import params
    >>> from unittest import TestCase
    >>> class TestMuted(TestCase):
    ...     @allure.id("56")
    ...     @params("one", "two")
    ...     def test_muted(self, value):
    ...         raise AssertionError("muted body ran")
    ...     def test_active(self):
    ...         pass
    """
    results = nose2_runner.run_docstring(module_name="muting", testplan={"mutedTests": [{"id": 56}]})

    muted = [result for result in results.test_cases if result["name"].startswith("test_muted")]
    assert len(muted) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] for result in muted)
    assert next(result for result in results.test_cases if result["name"] == "test_active")["status"] == "passed"
