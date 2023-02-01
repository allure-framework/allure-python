""" ./allure-pytest-bdd/examples/scenario-outline """

from hamcrest import assert_that, all_of
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step
from allure_commons_test.result import has_parameter


def test_scenario_outline(executed_docstring_directory):
    assert_that(
        executed_docstring_directory.allure_report,
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