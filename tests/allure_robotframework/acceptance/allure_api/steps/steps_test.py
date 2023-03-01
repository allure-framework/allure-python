""" ./allure-robotframework/examples/step.rst """

from hamcrest import assert_that
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step


def test_library_steps(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"steps.robot": "steps-robot"},
        library_rst_ids={"my_lib.py": "steps-lib"}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Steps.Allure substeps",
            has_step(
                "my_lib.Substep",
                has_step(
                    "Library substep",
                    has_step("Substep 'A'")
                )
            )
        )
    )
