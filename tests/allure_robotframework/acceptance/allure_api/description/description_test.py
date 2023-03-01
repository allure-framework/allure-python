""" ./allure-robotframework/examples/description.rst """

from hamcrest import assert_that
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description


def test_single_line_description_from_setting(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"description.robot": "setting-singleline-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Description.Single line doc from the setting",
            has_description(
                "This documentation will appear as allure description"
            )
        )
    )


def test_miltiline_description_from_setting(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"description.robot": "setting-multiline-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Description.Multiline doc from the setting",
            has_description(
                "This documentation contains multiple lines of text.\n"
                "It will also appear as allure description."
            )
        )
    )


def test_miltiline_description_from_keyword(
    robot_runner: AllureRobotRunner
):
    robot_runner.run_robotframework(
        suite_rst_ids={"description.robot": "keyword-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Description.Multiline doc from the keyword",
            has_description(
                "This documentation will appear as allure description."
            )
        )
    )
