""" ./allure-behave/examples/description """

from tests.allure_behave.conftest import AllureBehaveRunner
from hamcrest import assert_that, all_of
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description


def test_descriptions_from_feature_file(executed_docstring_path: AllureBehaveRunner):
    assert_that(
        executed_docstring_path.allure_results,
        has_test_case(
            "Description from a .feature file",
            has_description("This scenario has a description.\nThis description spans across multiple lines.")
        )
    )


def test_descriptions_from_step(executed_docstring_path: AllureBehaveRunner):
    assert_that(
        executed_docstring_path.allure_results,
        has_test_case(
            "Description from a step definition function",
            has_description(
                "This scenario has a description specified by a step definition"
            )
        )
    )


def test_descriptions_before_scenario(executed_docstring_path: AllureBehaveRunner):
    assert_that(
        executed_docstring_path.allure_results,
        has_test_case(
            "Description from before_scenario hook",
            has_description(
                "This scenario has a description specified in before_scenario hook"
            )
        )
    )


def test_descriptions_after_scenario(executed_docstring_path: AllureBehaveRunner):
    assert_that(
        executed_docstring_path.allure_results,
        has_test_case(
            "Description from after_scenario hook",
            has_description(
                "This scenario has a description specified in after_scenario hook"
            )
        )
    )
