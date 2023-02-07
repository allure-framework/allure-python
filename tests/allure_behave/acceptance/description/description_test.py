""" ./allure-behave/examples/description.rst """

from tests.allure_behave.conftest import AllureBehaveRunner
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description
from allure_commons_test.result import with_status

def test_descriptions_from_feature_file(behave_runner: AllureBehaveRunner):
    behave_runner.run_rst_example(
        "description-in-feature-feature",
        steps=["description-in-feature-steps"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Description from a .feature file",
            with_status("passed"),
            has_description(
                "This scenario has a description.\nThis description spans "
                "across multiple lines."
            )
        )
    )


def test_descriptions_from_step(behave_runner: AllureBehaveRunner):
    behave_runner.run_rst_example(
        "description-in-step-feature",
        steps=["description-in-step-steps"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Description from a step definition",
            with_status("passed"),
            has_description(
                "This scenario has a description specified by the step "
                "definition"
            )
        )
    )


def test_descriptions_before_scenario(behave_runner: AllureBehaveRunner):
    behave_runner.run_rst_example(
        "description-in-hook-feature",
        steps=["description-in-feature-steps"],
        environment="description-in-hook-env"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Description from the before_scenario hook",
            with_status("passed"),
            has_description(
                "This scenario has a description specified in the before_scenario hook"
            )
        )
    )


def test_descriptions_after_scenario(behave_runner: AllureBehaveRunner):
    behave_runner.run_rst_example(
        "description-in-hook-feature",
        steps=["description-in-feature-steps"],
        environment="description-in-hook-env"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Description from the after_scenario hook",
            with_status("passed"),
            has_description(
                "This scenario has a description specified in the "
                "after_scenario hook"
            )
        )
    )
