from hamcrest import assert_that
from doctest import script_from_examples
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains
from allure_commons_test.result import has_step


def test_failed_test(docstring, robot_runner: AllureRobotRunner):
    """
    *** Test Cases ***
    Failed Test Case
        Fail    msg=Reason
    """

    robot_runner.run_robotframework(
        suite_literals={"status.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Status.Failed Test Case",
            with_status("failed"),
            has_status_details(
                with_message_contains("Reason"),
                with_trace_contains("AssertionError: Reason")
            )
        )
    )


def test_failed_in_library(docstring, robot_runner: AllureRobotRunner):
    """
    *** Settings ***
    Library     ./library.py

    *** Test Cases ***
    Failed Test Case
        Fail In Library
    """

    library = script_from_examples(
        """
        >>> from robot.libraries.BuiltIn import BuiltIn
        >>> def fail_in_library():
        ...     BuiltIn().fail("Reason")
        """
    )

    robot_runner.run_robotframework(
        suite_literals={"status.robot": docstring},
        library_literals={"library.py": library}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Status.Failed Test Case",
            with_status("failed"),
            has_status_details(
                with_message_contains("Reason"),
                with_trace_contains("library.py\", line 3, in fail_in_library")
            ),
            has_step(
                "library.Fail In Library",
                with_status("failed"),
                has_status_details(
                    with_message_contains("Reason"),
                    with_trace_contains("library.py\", line 3, in fail_in_library")
                )
            )
        )
    )


def test_steps_after_failed_are_skipped(docstring, robot_runner: AllureRobotRunner):
    """
    *** Test Cases ***
    Failed Test Case
        Fail
        Log     This step is skipped
    """

    robot_runner.run_robotframework(
        suite_literals={"status.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Status.Failed Test Case",
            has_step(
                "BuiltIn.Log",
                with_status("skipped")
            )
        )
    )


def test_only_failed_steps_have_status_details(docstring, robot_runner: AllureRobotRunner):
    """
    *** Variables ***
    @{TEST_VALUES}    0    5    15

    *** Test Cases ***
    Test Case with mixed step results and status details
        FOR    ${value}    IN    @{TEST_VALUES}
            Run Keyword And Ignore Error    Should Be True    ${value} > 10
        END
        Log To Console    Test message
    """

    robot_runner.run_robotframework(
        suite_literals={"status.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Test Case with mixed step results and status details",
            has_step(
                "${value}    IN    @{TEST_VALUES}",
                has_step(
                    "${value} = 0",
                    has_step(
                        "BuiltIn.Run Keyword And Ignore Error",
                        has_step(
                            "BuiltIn.Should Be True",
                            with_status("failed"),
                            has_status_details(
                                with_message_contains("0 > 10' should be true."),
                            )
                        ),
                    ),
                ),
                has_step(
                    "${value} = 5",
                    has_step(
                        "BuiltIn.Run Keyword And Ignore Error",
                        has_step(
                            "BuiltIn.Should Be True",
                            with_status("failed"),
                            has_status_details(
                                with_message_contains("5 > 10' should be true."),
                            )
                        ),
                    ),
                ),
                has_step(
                    "${value} = 15",
                    has_step(
                        "BuiltIn.Run Keyword And Ignore Error",
                        has_step(
                            "BuiltIn.Should Be True",
                            with_status("passed"),
                            has_status_details({})
                        ),
                    ),
                )
            ),
            has_step(
                "BuiltIn.Log To Console",
                with_status("passed"),
                has_status_details({})
            )
        )
    )
