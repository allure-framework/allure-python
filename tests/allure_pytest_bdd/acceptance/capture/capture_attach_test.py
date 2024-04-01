import pytest
from hamcrest import assert_that, empty
from hamcrest import all_of, is_, is_not
from hamcrest import has_property, has_value
from hamcrest import contains_string
from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize("capture", ["sys", "fd", "no"])
def test_capture_stdout_in_bdd(allure_pytest_bdd_runner: AllurePytestRunner, capture):
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
            print("Print from given step")

        @when("the action is invoked")
        def when_the_action_is_invoked():
            print("Print from when step")

        @then("the postconditions are held")
        def then_the_postconditions_are_held():
            print("Print from then step")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", feature_content),
        steps_content, cli_args=(f"--capture={capture}",)
    )
    if_pytest_capture_ = is_not if capture == "no" else is_

    assert_that(
        allure_results,
        has_property(
            "attachments",
            all_of(
                if_pytest_capture_(has_value(contains_string("Print from given step"))),
                if_pytest_capture_(has_value(contains_string("Print from when step"))),
                if_pytest_capture_(has_value(contains_string("Print from then step")))
            )
        )
    )


@pytest.mark.parametrize("capture", ["sys", "fd"])
def test_capture_empty_stdout(allure_pytest_bdd_runner: AllurePytestRunner, capture):
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

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", feature_content),
        steps_content, cli_args=(f"--capture={capture}",)
    )

    assert_that(
        allure_results,
        has_property("attachments", empty())
    )


@pytest.mark.parametrize("logging", [True, False])
def test_capture_log(allure_pytest_bdd_runner: AllurePytestRunner, logging):
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
        import logging
        from pytest_bdd import scenario, given, when, then
        logger = logging.getLogger(__name__)
        @scenario("scenario.feature", "Simple passed example")
        def test_scenario_passes():
            pass

        @given("the preconditions are satisfied")
        def given_the_preconditions_are_satisfied():
            logging.info("Logging from given step")

        @when("the action is invoked")
        def when_the_action_is_invoked():
            logging.info("Logging from when step")

        @then("the postconditions are held")
        def then_the_postconditions_are_held():
            logging.info("Logging from then step")
        """
    )

    log_level = "INFO" if logging else "WARNING"
    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("scenario.feature", feature_content),
        steps_content, cli_args=(f"--log-level={log_level}",)
    )

    if_logging_ = is_ if logging else is_not

    assert_that(
        allure_results,
        has_property(
            "attachments",
            all_of(
                if_logging_(has_value(contains_string("Logging from given step"))),
                if_logging_(has_value(contains_string("Logging from when step"))),
                if_logging_(has_value(contains_string("Logging from then step"))),
            )
        )
    )
