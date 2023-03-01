""" ./allure-robotframework/examples/label.rst """

from allure import severity_level
from hamcrest import assert_that
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label
from allure_commons_test.label import has_feature
from allure_commons_test.label import has_story
from allure_commons_test.label import has_severity
from allure_commons_test.label import has_suite


def test_custom_label_from_robot_tag(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"labels.robot": "tag-custom-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Labels.Test authored by John Doe",
            has_label("author", "John Doe")
        )
    )


def test_builtin_label_from_robot_tag(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"labels.robot": "tag-builtin-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Labels.Test with the pinned ID",
            has_label("as_id", "1008"),
            has_story("RF tags as allure labels")
        )
    )


def test_robot_tag_from_settings(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"labels.robot": "tag-setting-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Labels.Test with two BDD-labels",
            has_feature("Allure labels support"),
            has_story("RF tags as allure labels")
        )
    )


def test_labels_from_test_library(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"labels.robot": "code-labels-robot"},
        library_rst_ids={"my_library.py": "code-labels-library"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Labels.Test backend API",
            has_label("layer", "API"),
            has_severity(severity_level.CRITICAL),
            has_label("endpoint", "localhost:443"),
            has_suite("Testing API at localhost")
        )
    )
