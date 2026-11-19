import pytest


@pytest.mark.parametrize("modifier", [False, True])
@pytest.mark.parametrize("entry", [{"id": 12}, {"id": "unknown", "selector": "Muting.Muted"}])
@pytest.mark.parametrize("selected", [False, True])
def test_muted_robot_tests(robot_runner, modifier, entry, selected):
    options = {"prerunmodifier": "allure_robotframework.testplan"} if modifier else {}
    plan = {"excludedTests": [entry, {"selector": "Muting.Outside"}]}
    if selected and modifier:
        plan["tests"] = [{"selector": "Muting.Muted"}, {"selector": "Muting.Active"}]
    results = robot_runner.run_robotframework(
        suite_literals={"muting.robot": """
*** Test Cases ***
Muted
    [Tags]    allure.id:12
    Fail    muted body ran
Active
    No Operation
Outside
    Fail    muted body ran
"""},
        testplan_content=plan,
        options=options
    )

    assert len(results.test_cases) == (2 if selected and modifier else 3)
    muted = next(result for result in results.test_cases if result["name"] == "Muted")
    assert muted["status"] == "skipped"
    assert muted["statusDetails"]["muted"] is True
    assert next(result for result in results.test_cases if result["name"] == "Active")["status"] == "passed"
