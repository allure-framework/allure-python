from hamcrest import assert_that, all_of, has_entry
from tests.allure_behave.behave_runner import AllureBehaveRunner
from allure_commons_test.report import has_only_testcases
from allure_commons_test.result import with_status
from allure_commons_test.result import has_parameter


def test_outline_with_single_table(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_paths=["./test-data/outline.feature"],
        step_paths=["./test-data/steps.py"],
        options=["--tags=1", "--no-skipped"]
    )

    assert_that(
        behave_runner.allure_results,
        has_only_testcases(
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with one table -- @1.1 Customers"
                ),
                with_status("passed"),
                has_parameter("name", "Alice"),
                has_parameter("surname", "Johnson")
            ),
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with one table -- @1.2 Customers"
                ),
                with_status("passed"),
                has_parameter("name", "Bob"),
                has_parameter("surname", "Smith")
            )
        )
    )


def test_outline_with_multiple_tables(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_paths=["./test-data/outline.feature"],
        step_paths=["./test-data/steps.py"],
        options=["--tags=multiple-tables", "--no-skipped"]
    )

    assert_that(
        behave_runner.allure_results,
        has_only_testcases(
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with multiple tables -- @1.1 Customers"
                ),
                with_status("passed"),
                has_parameter("name", "Alice"),
                has_parameter("surname", "Johnson")
            ),
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with multiple tables -- @1.2 Customers"
                ),
                with_status("passed"),
                has_parameter("name", "Bob"),
                has_parameter("surname", "Smith")
            ),
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with multiple tables -- @2.1 Employees"
                ),
                with_status("passed"),
                has_parameter("name", "Jane"),
                has_parameter("surname", "Watson")
            ),
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with multiple tables -- @2.2 Employees"
                ),
                with_status("passed"),
                has_parameter("name", "Mark"),
                has_parameter("surname", "Nickson")
            )
        )
    )


def test_multiple_outlines_each_with_one_table(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_paths=["./test-data/outline.feature"],
        step_paths=["./test-data/steps.py"],
        options=["--tags=single-table", "--no-skipped"]
    )

    assert_that(
        behave_runner.allure_results,
        has_only_testcases(
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with one table -- @1.1 Customers"
                ),
                with_status("passed"),
                has_parameter("name", "Alice"),
                has_parameter("surname", "Johnson")
            ),
            all_of(
                has_entry(
                    "name",
                    "Scenario outline with one table -- @1.2 Customers"
                ),
                with_status("passed"),
                has_parameter("name", "Bob"),
                has_parameter("surname", "Smith")
            ),
            all_of(
                has_entry(
                    "name",
                    "Another scenario outline with one table -- @1.1 Employees"
                ),
                with_status("passed"),
                has_parameter("name", "Jane"),
                has_parameter("surname", "Watson")
            ),
            all_of(
                has_entry(
                    "name",
                    "Another scenario outline with one table -- @1.2 Employees"
                ),
                with_status("passed"),
                has_parameter("name", "Mark"),
                has_parameter("surname", "Nickson")
            )
        )
    )
