import allure
from tests.allure_behave.conftest import AllureBehaveRunner
from hamcrest import assert_that, equal_to
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_step
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import has_attachment_with_content
from allure_commons_test.content import csv_equivalent

def test_failed_behave_step(docstring:str, behave_runner: AllureBehaveRunner):
    """
    Feature: Bheave step support
        Scenario: Scenario with failed step
            Given a step failed
    """

    behave_runner.run_behave(
        features=[docstring],
        steps=["@given('a step failed')\ndef _(_):assert False,'Fail message'"]
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with failed step",
            with_status("failed"),
            has_step(
                "Given a step failed",
                with_status("failed"),
                has_status_details(
                    with_message_contains("AssertionError: Fail message")
                )
            )
        )
    )

def test_broken_behave_step(docstring:str, behave_runner: AllureBehaveRunner):
    """
    Feature: Bheave step support
        Scenario: Scenario with broken step
            Given a broken step
    """

    behave_runner.run_behave(
        features=[docstring],
        steps=["@given('a broken step')\ndef _(_):raise ValueError('Reason')"]
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with broken step",
            with_status("broken"),
            has_step(
                "Given a broken step",
                with_status("broken"),
                has_status_details(
                    with_message_contains("ValueError: Reason")
                )
            )
        )
    )


def test_step_text_data(docstring:str, behave_runner: AllureBehaveRunner):
    """
    Feature: Bheave step support
        Scenario: Scenario with step which contains text data
            Given a step with text data
                '''
                Textual information attached to the step.
                '''
    """

    behave_runner.run_behave(
        features=[docstring],
        steps=["given('a step with text data')(lambda _:0)"]
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with step which contains text data",
            with_status("passed"),
            has_step(
                "Given a step with text data",
                with_status("passed"),
                has_attachment_with_content(
                    behave_runner.allure_results.attachments,
                    equal_to("Textual information attached to the step."),
                    "text/plain"
                )
            )
        )
    )


def test_step_table_data(docstring:str, behave_runner: AllureBehaveRunner):
    """
    Feature: Bheave step support
        Scenario: Scenario with step which contains a table
            Given a step with table data
                | id | name |
                | 1  | John |
                | 2  | Jane |
    """

    behave_runner.run_behave(
        features=[docstring],
        steps=["given('a step with table data')(lambda _:0)"]
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with step which contains a table",
            with_status("passed"),
            has_step(
                "Given a step with table data",
                with_status("passed"),
                has_attachment_with_content(
                    behave_runner.allure_results.attachments,
                    csv_equivalent([
                        ["id", "name"],
                        ["1", "John"],
                        ["2", "Jane"]
                    ]),
                    "text/csv"
                )
            )
        )
    )


@allure.issue("https://github.com/allure-framework/allure-python/issues/717")
def test_step_table_data_escaping(
    docstring:str,
    behave_runner: AllureBehaveRunner
):
    """
    Feature: Bheave step support
        Scenario: Csv special symbols in step's table data
            Given a step table data with special symbols
                | Item A           | Item B          |
                | Item "1", Item 2 | Item 3," Item 4 |
    """

    behave_runner.run_behave(
        features=[docstring],
        steps=["given('a step table data with special symbols')(lambda _:0)"]
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Csv special symbols in step's table data",
            with_status("passed"),
            has_step(
                "Given a step table data with special symbols",
                has_attachment_with_content(
                    behave_runner.allure_results.attachments,
                    csv_equivalent([
                        ["Item A", "Item B"],
                        ["Item \"1\", Item 2", "Item 3,\" Item 4"]
                    ]),
                    "text/csv"
                )
            )
        )
    )
