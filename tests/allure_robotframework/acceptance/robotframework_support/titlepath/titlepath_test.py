from hamcrest import assert_that, all_of
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title_path


def test_titlepath_of_directly_run_suite(docstring, robot_runner: AllureRobotRunner):
    """
    *** Test Cases ***
    Bar
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"foo.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Bar",
            has_title_path("Foo"),
        )
    )


def test_titlepath_of_nested_suites(docstring, robot_runner: AllureRobotRunner):
    """
    *** Test Cases ***
    Qux
        No Operation
    """

    robot_runner.rootdir = "foo"

    robot_runner.run_robotframework(
        suite_literals={
            "foo/bar/baz.robot": docstring,
            "foo/bor/buz.robot": docstring,
        }

    )

    assert_that(
        robot_runner.allure_results,
        all_of(
            has_test_case(
                "Foo.Bar.Baz.Qux",
                has_title_path("Foo", "Bar", "Baz"),
            ),
            has_test_case(
                "Foo.Bor.Buz.Qux",
                has_title_path("Foo", "Bor", "Buz"),
            ),
        ),
    )
