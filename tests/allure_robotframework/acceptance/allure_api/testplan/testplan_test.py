""" ./allure-robotframework/examples/testplan.rst """

from allure_commons_test.report import has_test_case
from hamcrest import assert_that, all_of, not_
from tests.allure_robotframework.robot_runner import AllureRobotRunner


def test_testplan(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_rst_ids={"testplan.robot": "testdata"},
        testplan_rst_id="testplan",
        options={"prerunmodifier": "allure_robotframework.testplan"}
    )

    assert_that(
        robot_runner.allure_results,
        all_of(
            has_test_case("Testplan.Selected by Name"),
            has_test_case("Selected by ID"),
            not_(
                has_test_case("Testplan.Not Selected")
            )
        )
    )
