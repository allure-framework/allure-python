""" ./allure-pytest-bdd/examples/simple-scenario """

from allure import issue
from hamcrest import assert_that, not_, equal_to
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
        steps_content,
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

@issue("925")
def test_uuid_not_reused_across_runs(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given, when, then

        @scenario("foo.feature", "Bar")
        def test_bar():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    output1 = allure_pytest_bdd_runner.run_pytest(
        ("foo.feature", feature_content),
        steps_content
    )
    output2 = allure_pytest_bdd_runner.run_pytest(
        ("foo.feature", feature_content),
        steps_content
    )

    uuid1 = output1.test_cases[0]["uuid"]
    uuid2 = output2.test_cases[0]["uuid"]

    assert_that(uuid1, not_(equal_to(uuid2)))
