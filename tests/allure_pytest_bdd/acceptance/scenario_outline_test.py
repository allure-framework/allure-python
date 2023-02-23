""" ./allure-pytest-bdd/examples/scenario-outline """

from hamcrest import assert_that, all_of
from tests.allure_pytest.pytest_runner import AllurePytestRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step
from allure_commons_test.result import has_parameter


def test_scenario_outline(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Allure report for scenario outline
            Scenario Outline: Two examples with two parameters each
                Given first step for <first> value
                When something is done with the value <second>
                Then check postconditions using <first> and <second>

                Examples:
                | first | second |
                | Alpha |      1 |
                | Bravo |      2 |
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given, when, then
        from pytest_bdd import parsers

        @scenario("outline.feature", "Two examples with two parameters each")
        def test_scenario_outline():
            pass

        @given(parsers.parse("first step for {first} value"))
        def given_first_step_for_first_value(first):
            pass

        @when(parsers.parse("something is done with the value {second}"))
        def when_something_is_done_with_the_value_second(second):
            pass

        @then(parsers.parse("check postconditions using {first} and {second}"))
        def then_check_postconditions_using_first_and_second(first, second):
            pass
        """
    )

    output = allure_pytest_bdd_runner.run_pytest(
        ("outline.feature", feature_content),
        steps_content,
    )

    assert_that(
        output,
        all_of(
            has_test_case(
                "Two examples with two parameters each",
                with_status("passed"),
                has_step("Given first step for Alpha value"),
                has_step("When something is done with the value 1"),
                has_step("Then check postconditions using Alpha and 1"),
                has_parameter("first", "Alpha"),
                has_parameter("second", "1")
            ),
            has_test_case(
                "Two examples with two parameters each",
                with_status("passed"),
                has_step("Given first step for Bravo value"),
                has_step("When something is done with the value 2"),
                has_step("Then check postconditions using Bravo and 2"),
                has_parameter("first", "Bravo"),
                has_parameter("second", "2")
            )
        )
    )
