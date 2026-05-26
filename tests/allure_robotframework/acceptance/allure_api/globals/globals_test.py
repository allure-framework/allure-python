""" ./allure-robotframework/examples/attachment.rst """

from hamcrest import assert_that, equal_to, has_item, has_length
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.result import has_global_attachment_with_content
from allure_commons_test.result import has_global_error
from allure_commons_test.result import with_message_contains


def test_global_attachment_and_error(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_literals={
            "global-attachment.robot": (
                """
                *** Settings ***
                Library     AllureLibrary
                Library     ./lib.py
                Suite Setup     Global Attach    robot global attachment    name=robot global
                Suite Teardown  Global Error     robot global error

                *** Test Cases ***
                Global Attachment
                    Add Globals From Code
                """
            ),
        },
        library_literals={
            "lib.py": (
                """
                import allure

                def add_globals_from_code():
                    allure.global_attach(body="global body", name="global attachment")
                    allure.global_error("message only error")
                """
            ),
        },
    )

    assert_that(robot_runner.allure_results.globals, has_length(4))

    assert_that(
        robot_runner.allure_results.globals,
        has_item(
            has_global_attachment_with_content(
                robot_runner.allure_results.attachments,
                equal_to("robot global attachment"),
                name="robot global"
            )
        )
    )
    assert_that(
        robot_runner.allure_results.globals,
        has_item(
            has_global_attachment_with_content(
                robot_runner.allure_results.attachments,
                equal_to("global body"),
                name="global attachment"
            )
        )
    )
    assert_that(
        robot_runner.allure_results.globals,
        has_item(
            has_global_error(
                with_message_contains("robot global error")
            )
        )
    )
    assert_that(
        robot_runner.allure_results.globals,
        has_item(
            has_global_error(
                with_message_contains("message only error")
            )
        )
    )
