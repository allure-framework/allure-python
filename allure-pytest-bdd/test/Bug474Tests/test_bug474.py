from pytest_bdd import scenario, then


@scenario("bug474.feature", "allure.attach calling in method decorated with When and Pytest.fixture")
def test_my_scenario():
    pass


@then("attachment must be only in when-step attachments")
def attachment_only_in_when(allure_report):
    test_case_report = allure_report.test_cases[0]
    when_step_report = next(step for step in test_case_report["steps"]
                            if step["name"].startswith("When"))

    assert "attachments" not in test_case_report.keys()
    assert len(when_step_report["attachments"]) == 1
    assert when_step_report["attachments"][0]["name"] == "blah blah blah"
