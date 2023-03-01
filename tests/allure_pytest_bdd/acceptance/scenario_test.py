""" ./allure-pytest-bdd/examples/simple-scenario """

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step
from allure_commons_test.result import has_history_id


def test_simple_passed_scenario(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Basic allure-pytest-bdd usage
            Scenario: Simple passed example
                Given the preconditions are satisfied
                When the action is invoked
                Then the postconditions are held
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given, when, then

        @scenario("scenario.feature", "Simple passed example")
        def test_scenario_passes():
            pass

        @given("the preconditions are satisfied")
        def given_the_preconditions_are_satisfied():
            pass

        @when("the action is invoked")
        def when_the_action_is_invoked():
            pass

        @then("the postconditions are held")
        def then_the_postconditions_are_held():
            pass
        """
    )

    output = allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", feature_content),
        steps_content
    )

    assert_that(
        output,
        has_test_case(
            "Simple passed example",
            with_status("passed"),
            has_step("Given the preconditions are satisfied"),
            has_step("When the action is invoked"),
            has_step("Then the postconditions are held"),
            has_history_id()
        )
    )
