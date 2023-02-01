""" ./allure-pytest-bdd/examples/simple-scenario """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step
from allure_commons_test.result import has_history_id


def test_simple_passed_scenario(executed_docstring_directory):
    assert_that(
        executed_docstring_directory.allure_report,
        has_test_case(
            "Simple passed example",
            with_status("passed"),
            has_step("Given the preconditions are satisfied"),
            has_step("When the action is invoked"),
            has_step("Then the postconditions are held"),
            has_history_id()
        )
    )