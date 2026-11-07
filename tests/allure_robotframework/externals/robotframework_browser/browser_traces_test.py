from hamcrest import assert_that, not_

from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_attachment


_SUITE_WITH_TRACE = """\
*** Settings ***
Library    fake_browser_library.py

*** Test Cases ***
Browser Trace Test
    Open Browser    about:blank
    Create Trace
    Close Browser
"""

_SUITE_WITHOUT_TRACE = """\
*** Settings ***
Library    fake_browser_library.py

*** Test Cases ***
Browser No Trace Test
    Open Browser    about:blank
    Do Nothing
    Close Browser
"""

_SUITE_WITH_TRACE_IN_SUBDIR = """\
*** Settings ***
Library    fake_browser_library.py

*** Test Cases ***
Browser Subdir Trace Test
    Open Browser    about:blank
    Create Trace In Subdir
    Close Browser
"""

_SUITE_FAILING_WITH_TRACE = """\
*** Settings ***
Library    fake_browser_library.py

*** Test Cases ***
Browser Failing Test
    Open Browser    about:blank
    Create Trace
    Fail    intentional failure
    Close Browser
"""


def test_trace_attached_when_browser_creates_zip(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_literals={"browser_trace.robot": _SUITE_WITH_TRACE},
        library_paths=["fake_browser_library.py"],
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Browser Trace Test",
            has_attachment(attach_type="application/vnd.allure.playwright-trace"),
        ),
    )


def test_trace_not_attached_when_no_zip_created(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_literals={"browser_no_trace.robot": _SUITE_WITHOUT_TRACE},
        library_paths=["fake_browser_library.py"],
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Browser No Trace Test",
            not_(has_attachment(attach_type="application/vnd.allure.playwright-trace")),
        ),
    )


def test_trace_attached_when_browser_creates_zip_in_subdir(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_literals={"browser_trace_subdir.robot": _SUITE_WITH_TRACE_IN_SUBDIR},
        library_paths=["fake_browser_library.py"],
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Browser Subdir Trace Test",
            has_attachment(attach_type="application/vnd.allure.playwright-trace"),
        ),
    )


def test_trace_attached_on_failing_test(robot_runner: AllureRobotRunner):
    robot_runner.run_robotframework(
        suite_literals={"browser_fail.robot": _SUITE_FAILING_WITH_TRACE},
        library_paths=["fake_browser_library.py"],
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Browser Failing Test",
            has_attachment(attach_type="application/vnd.allure.playwright-trace"),
        ),
    )
