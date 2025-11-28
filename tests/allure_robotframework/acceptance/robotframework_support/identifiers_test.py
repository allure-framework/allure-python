from hamcrest import assert_that
from hamcrest import all_of
from hamcrest import contains_string
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_full_name
from allure_commons_test.result import has_test_case_id
from allure_commons_test.result import has_history_id


def test_identifiers_are_set(docstring, robot_runner: AllureRobotRunner):
    """
    *** Test Cases ***
    Foo
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"Bar.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Foo",
            has_full_name(
                all_of(
                    contains_string("Foo"),
                    contains_string("Bar"),
                ),
            ),
            has_test_case_id(),
            has_history_id(),
        )
    )
