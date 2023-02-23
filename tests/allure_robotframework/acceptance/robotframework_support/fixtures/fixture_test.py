from hamcrest import assert_that
from tests.allure_robotframework.robot_runner import AllureRobotRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.container import has_container
from allure_commons_test.container import has_before
from allure_commons_test.container import has_after
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains


def test_setup(docstring, robot_runner: AllureRobotRunner):
    """
    *** Keywords ***
    Fixture
        No Operation

    *** Test Cases ***
    Test Under Test
        [Setup]     Fixture
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"fixture.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Fixture.Test Under Test",
            has_container(
                robot_runner.allure_results,
                has_before(
                    "Fixture",
                    with_status("passed")
                )
            )
        )
    )


def test_failed_setup(docstring, robot_runner: AllureRobotRunner):
    """
    *** Keywords ***
    Fixture
        Fail  Reason

    *** Test Cases ***
    Test Under Test
        [Setup]     Fixture
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"fixture.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Fixture.Test Under Test",
            has_container(
                robot_runner.allure_results,
                has_before(
                    "Fixture",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("Reason")
                    )
                )
            )
        )
    )


def test_teardown(docstring, robot_runner: AllureRobotRunner):
    """
    *** Keywords ***
    Fixture
        No Operation

    *** Test Cases ***
    Test Under Test
        [Teardown]  Fixture
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"fixture.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Fixture.Test Under Test",
            has_container(
                robot_runner.allure_results,
                has_after(
                    "Fixture",
                    with_status("passed")
                )
            )
        )
    )


def test_failed_teardown(docstring, robot_runner: AllureRobotRunner):
    """
    *** Keywords ***
    Fixture
        Fail  Reason

    *** Test Cases ***
    Test Under Test
        [Teardown]  Fixture
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"fixture.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Fixture.Test Under Test",
            has_container(
                robot_runner.allure_results,
                has_after(
                    "Fixture",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("Reason")
                    )
                )
            )
        )
    )


def test_setup_teardown(docstring, robot_runner: AllureRobotRunner):
    """
    *** Keywords ***
    Setup Fixture
        No Operation

    Teardown Fixture
        No Operation

    *** Test Cases ***
    Test Under Test
        [Setup]     Setup Fixture
        [Teardown]  Teardown Fixture
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"fixture.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Fixture.Test Under Test",
            has_container(
                robot_runner.allure_results,
                has_before(
                    "Setup Fixture",
                    with_status("passed")
                ),
                has_after(
                    "Teardown Fixture",
                    with_status("passed")
                )
            )
        )
    )


def test_failed_setup_teardown(docstring, robot_runner: AllureRobotRunner):
    """
    *** Keywords ***
    Setup Fixture
        Fail  Setup fail reason

    Teardown Fixture
        Fail  Teardown fail reason

    *** Test Cases ***
    Test Under Test
        [Setup]     Setup Fixture
        [Teardown]  Teardown Fixture
        No Operation
    """

    robot_runner.run_robotframework(
        suite_literals={"fixture.robot": docstring}
    )

    assert_that(
        robot_runner.allure_results,
        has_test_case(
            "Fixture.Test Under Test",
            has_container(
                robot_runner.allure_results,
                has_before(
                    "Setup Fixture",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("Setup fail reason")
                    )
                ),
                has_after(
                    "Teardown Fixture",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("Teardown fail reason")
                    )
                )
            )
        )
    )
