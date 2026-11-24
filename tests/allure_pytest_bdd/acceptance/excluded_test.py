import os
import pytest

from tests.e2e import version_gte


@pytest.mark.parametrize("entry", [{"id": 12}, {"id": "missing", "selector": "exclusion.feature:Excluded"}])
@pytest.mark.parametrize("selection", [None, []])
@pytest.mark.parametrize("workers", [False, True])
def test_excluded_scenario_bodies(allure_pytest_bdd_runner, entry, selection, workers):
    if workers:
        allure_pytest_bdd_runner.in_memory = False
        allure_pytest_bdd_runner.enable_plugins("xdist")
    entry = dict(entry)
    if "selector" in entry and version_gte("pytest-bdd", 8):
        entry["selector"] = os.path.join(allure_pytest_bdd_runner.pytester.path.name, entry["selector"])
    plan = {"excludedTests": [entry]}
    if selection is not None:
        plan["tests"] = selection
    results = allure_pytest_bdd_runner.run_pytest(
        ("exclusion.feature", """
Feature: Exclusion
  Scenario Outline: Excluded
    Given forbidden <value>
    Examples:
      | value |
      | one   |
      | two   |
  Scenario: Active
    Given allowed
"""),
        """
import allure
from pytest_bdd import scenario, given, parsers
@allure.id("12")
@scenario("exclusion.feature", "Excluded")
def test_excluded():
    pass
@scenario("exclusion.feature", "Active")
def test_active():
    pass
@given(parsers.parse("forbidden {value}"))
def forbidden(value):
    raise AssertionError("excluded step ran")
@given("allowed")
def allowed():
    pass
""", testplan=plan, cli_args=["-n2"] if workers else []
    )

    excluded = [result for result in results.test_cases if result["name"] == "Excluded"]
    assert len(results.test_cases) == 3
    assert len(excluded) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] is True for result in excluded)
    assert all(result.get("stop") and result.get("historyId") for result in excluded)
    assert next(result for result in results.test_cases if result["name"] == "Active")["status"] == "passed"
