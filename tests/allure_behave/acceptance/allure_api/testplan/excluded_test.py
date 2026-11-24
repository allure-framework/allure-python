import pytest


@pytest.mark.parametrize("entry", [{"id": 12}, {"id": "unknown", "selector": "Exclusion: Excluded scenario"}])
@pytest.mark.parametrize("selected", [False, True])
def test_excluded_scenarios(behave_runner, entry, selected):
    plan = {"excludedTests": [entry, {"selector": "Exclusion: Outside"}]}
    if selected:
        plan["tests"] = [{"selector": "Exclusion: Excluded scenario"}, {"selector": "Exclusion: Active"}]

    results = behave_runner.run_behave(
        feature_literals=["""
Feature: Exclusion
  @allure.id:12
  Scenario Outline: Excluded scenario
    Given forbidden <value>
    Examples:
      | value |
      | one   |
      | two   |
  Scenario: Active
    Given allowed
  Scenario: Outside
    Given forbidden outside
"""],
        step_literals=["""
from behave import given
@given('forbidden {value}')
def forbidden(context, value):
    raise AssertionError('excluded step ran')
@given('allowed')
def allowed(context):
    pass
"""],
        testplan_content=plan,
        options=["-D", "AllureFormatter.hide_excluded=True"]
    )

    excluded = [result for result in results.test_cases if result["name"].startswith("Excluded")]
    assert len(results.test_cases) == (3 if selected else 4)
    assert len(excluded) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] is True for result in excluded)
    assert next(result for result in results.test_cases if result["name"] == "Active")["status"] == "passed"
