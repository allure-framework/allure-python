""" ./allure-robotframework/examples/link.rst """

from hamcrest import assert_that
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link
from allure_commons_test.result import has_issue_link
from allure_commons_test.result import has_test_case_link


def test_link_from_robot_tag(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"links.robot": "tag-unnamed-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Links.Allure Plain Link",
            has_link(
                "https://github.com/allure-framework/allure-python",
                "link",
                "https://github.com/allure-framework/allure-python"
            )
        )
    )


def test_named_link_from_robot_tag(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"links.robot": "tag-named-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Links.Allure Plain Link",
            has_link(
                "https://github.com/allure-framework/allure-python",
                "link",
                "allure-python"
            )
        )
    )


def test_issue_from_robot_tag(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"links.robot": "tag-issue-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Links.Allure Issue Link",
            has_issue_link(
                "https://github.com/allure-framework/allure-python/issues/1",
                "ISSUE-1"
            )
        )
    )


def test_tms_from_robot_tag(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"links.robot": "tag-tms-robot"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Links.Allure TMS Link",
            has_test_case_link(
                "https://my-tms/test-cases/1",
                "TESTCASE-1"
            )
        )
    )


def test_links_from_code(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"links.robot": "code-links-robot"},
        library_rst_ids={"my_lib.py": "code-links-lib"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Links.Allure Link Decorators and Functions",
            has_link(
                "https://github.com/allure-framework/allure-python",
                "link",
                "allure-python"
            ),
            has_issue_link(
                "https://github.com/allure-framework/allure-python/issues/1",
                "ISSUE-1"
            ),
            has_test_case_link(
                "https://my-tms/test-cases/1",
                "TESTCASE-1"
            )
        )
    )


def test_rf_specific_tag_syntax(docstring, robot_runner: AllureRobotRunner):
    """
    *** Test Cases ***
    RF-Specific Tag Syntax
        [Tags]  link:[allure-python]https://github.com/allure-framework/allure-python
        ...     link:https://github.com/allure-framework/allure-python/issues
        ...     issue:ISSUE-1
        ...     issue:https://github.com/allure-framework/allure-python/issues/1
        ...     issue:[ISSUE-1]https://github.com/allure-framework/allure-python/issues/1
        ...     tms:TESTCASE-1
        ...     tms:https://my-tms/test-cases/1
        ...     tms:[TESTCASE-1]https://my-tms/test-cases/1
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"links.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Links.RF-Specific Tag Syntax",
            has_link(
                "https://github.com/allure-framework/allure-python",
                "link",
                "allure-python"
            ),
            has_link(
                "https://github.com/allure-framework/allure-python/issues",
                "link",
                "https://github.com/allure-framework/allure-python/issues"
            )
        )
    )
