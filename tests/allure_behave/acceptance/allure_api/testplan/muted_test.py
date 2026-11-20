import pytest


@pytest.mark.parametrize("entry", [{"id": 12}, {"id": "unknown", "selector": "Muting: Muted scenario"}])
@pytest.mark.parametrize("selected", [False, True])
def test_muted_scenarios(behave_runner, entry, selected):
    plan = {"excludedTests": [entry, {"selector": "Muting: Outside"}]}
    if selected:
        plan["tests"] = [{"selector": "Muting: Muted scenario"}, {"selector": "Muting: Active"}]

    results = behave_runner.run_behave(
        feature_literals=["""
Feature: Muting
  @allure.id:12
  Scenario Outline: Muted scenario
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
    raise AssertionError('muted step ran')
@given('allowed')
def allowed(context):
    pass
"""],
        testplan_content=plan,
        options=["-D", "AllureFormatter.hide_excluded=True"]
    )

    muted = [result for result in results.test_cases if result["name"].startswith("Muted")]
    assert len(results.test_cases) == (3 if selected else 4)
    assert len(muted) == 2
    assert all(result["status"] == "skipped" and result["statusDetails"]["muted"] is True for result in muted)
    assert next(result for result in results.test_cases if result["name"] == "Active")["status"] == "passed"
