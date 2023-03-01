""" ./allure-robotframework/examples/tag.rst """

from hamcrest import assert_that, all_of, not_
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_tag
from allure_commons_test.label import has_label


def test_robot_tags(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"tags.robot": "tags-static-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Tags.Distributed Legacy Test",
            has_tag("distributed"),
            has_tag("legacy")
        )
    )


def test_modified_robot_tags(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"tags.robot": "tags-dynamic-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Tags.Isolated Test",
            all_of(
                has_tag("isolated"),
                not_(
                    has_tag("distributed")
                )
            )
        )
    )


def test_robot_tags_not_modified_because_of_failure(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"tags.robot": "tags-partial-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Tags.Supposed to Be an Isolated Test",
            all_of(
                has_tag("distributed"),
                not_(
                    has_tag("isolated")
                )
            )
        )
    )


def test_explicit_tags(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"tags.robot": "tags-explicit-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Tags.Explicit External Test",
            all_of(
                has_tag("explicit"),
                has_tag("extrenal")
            )
        )
    )


def test_rf_tags_starting_with_allure_not_added(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"tags.robot": "tags-noconv-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Tags.No Allure Tags",
            not_(
                has_label("tag")
            )
        )
    )


def test_tags_from_library(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"tags.robot": "tags-code-robot"},
        library_rst_ids={"my_lib.py": "tags-code-lib"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Tags.Stateful External Legacy Test",
            all_of(
                has_tag("stateful"),
                has_tag("external"),
                has_tag("legacy")
            )
        )
    )
