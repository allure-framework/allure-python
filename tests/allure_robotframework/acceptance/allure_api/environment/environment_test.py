from hamcrest import assert_that, has_entries
from tests.allure_robotframework.robot_runner import AllureRobotRunner


def test_environment_from_keyword_and_code(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_literals={
            "environment.robot": (
                """
                *** Settings ***
                Library     AllureLibrary
                Library     ./lib.py
                Suite Setup     Environment    browser=chrome    stand=staging

                *** Test Cases ***
                Environment
                    Add Environment From Code
                """
            ),
        },
        library_literals={
            "lib.py": (
                """
                import allure

                def add_environment_from_code():
                    allure.environment({"os.name": "Windows 11"}, browser="firefox")
                """
            ),
        },
    )

    assert_that(
        robot_runner.allure_results.environment,
        has_entries({
            "browser": "firefox",
            "stand": "staging",
            "os.name": "Windows 11",
        }),
    )
