from hamcrest import assert_that, equal_to

from allure_commons_test.report import has_test_case
from allure_commons_test.result import (
    has_preconditions, has_preconditions_html, has_expected_results, has_expected_results_html, with_status,
)


def test_dynamic_preconditions(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    documentation.py

            *** Test Cases ***
            Documentation
                Set Documentation
        """},
        library_literals={"documentation.py": """
            import allure

            def set_documentation():
                allure.dynamic.preconditions("Previous Preconditions")
                allure.dynamic.preconditions("Preconditions")
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Documentation",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_dynamic_preconditions_html(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    documentation.py

            *** Test Cases ***
            Documentation
                Set Documentation
        """},
        library_literals={"documentation.py": """
            import allure

            def set_documentation():
                allure.dynamic.preconditions_html("<p>Previous Preconditions</p>")
                allure.dynamic.preconditions_html("<p>Preconditions</p>")
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Documentation",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_dynamic_expected_results(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    documentation.py

            *** Test Cases ***
            Documentation
                Set Documentation
        """},
        library_literals={"documentation.py": """
            import allure

            def set_documentation():
                allure.dynamic.expected_results("Previous Expected results")
                allure.dynamic.expected_results("Expected results")
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Documentation",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_dynamic_expected_results_html(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    documentation.py

            *** Test Cases ***
            Documentation
                Set Documentation
        """},
        library_literals={"documentation.py": """
            import allure

            def set_documentation():
                allure.dynamic.expected_results_html("<p>Previous Expected results</p>")
                allure.dynamic.expected_results_html("<p>Expected results</p>")
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Documentation",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )


def test_preconditions_keyword(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    AllureLibrary

            *** Test Cases ***
            Preconditions
                Preconditions    Previous Preconditions
                Preconditions    Preconditions
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Preconditions",
            with_status("passed"),
            has_preconditions(equal_to("Preconditions")),
        ),
    )


def test_preconditions_html_keyword(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    AllureLibrary

            *** Test Cases ***
            Preconditions HTML
                Preconditions Html    <p>Previous Preconditions</p>
                Preconditions Html    <p>Preconditions</p>
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Preconditions HTML",
            with_status("passed"),
            has_preconditions_html(equal_to("<p>Preconditions</p>")),
        ),
    )


def test_expected_results_keyword(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    AllureLibrary

            *** Test Cases ***
            Expected results
                Expected Results    Previous Expected results
                Expected Results    Expected results
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Expected results",
            with_status("passed"),
            has_expected_results(equal_to("Expected results")),
        ),
    )


def test_expected_results_html_keyword(robot_runner):
    results = robot_runner.run_robotframework(
        suite_literals={"documentation.robot": """
            *** Settings ***
            Library    AllureLibrary

            *** Test Cases ***
            Expected results HTML
                Expected Results Html    <p>Previous Expected results</p>
                Expected Results Html    <p>Expected results</p>
        """},
    )

    assert_that(
        results,
        has_test_case(
            "Documentation.Expected results HTML",
            with_status("passed"),
            has_expected_results_html(equal_to("<p>Expected results</p>")),
        ),
    )
