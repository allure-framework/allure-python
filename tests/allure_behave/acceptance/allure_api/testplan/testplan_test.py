""" ./allure-behave/examples/testplan.rst """

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from hamcrest import assert_that, all_of, not_
from pytest import MonkeyPatch
from tests.allure_behave.conftest import AllureBehaveRunner
from tests.conftest import RstExampleTable

def test_testplan_fullname_selection(
    monkeypatch: MonkeyPatch,
    rst_examples: RstExampleTable,
    behave_runner: AllureBehaveRunner
):
    monkeypatch.setenv(
        "ALLURE_TESTPLAN_PATH",
        str(
            behave_runner.pytester.makefile(
                ".json",
                rst_examples["fullname-testplan"]
            )
        )
    )

    behave_runner.run_rst_example(
        "fullname-feature-1",
        "fullname-feature-2",
        steps=["steps"]
    )

    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario selection",
                with_status("passed")
            ),
            has_test_case(
                "Scenario deselection",
                with_status("skipped")
            ),
            has_test_case(
                "Scenario selection 2",
                with_status("passed")
            ),
            has_test_case(
                "Scenario deselection 2",
                with_status("skipped")
            )
        )
    )


def test_testplan_id_selection(
    monkeypatch: MonkeyPatch,
    rst_examples: RstExampleTable,
    behave_runner: AllureBehaveRunner
):
    monkeypatch.setenv(
        "ALLURE_TESTPLAN_PATH",
        str(
            behave_runner.pytester.makefile(
                ".json",
                rst_examples["id-testplan"]
            )
        )
    )

    behave_runner.run_rst_example(
        "id-feature-1",
        "id-feature-2",
        steps=["steps"]
    )

    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario selection",
                with_status("passed")
            ),
            has_test_case(
                "Scenario deselection",
                with_status("skipped")
            ),
            has_test_case(
                "Scenario selection 2",
                with_status("passed")
            ),
            has_test_case(
                "Scenario deselection 2",
                with_status("skipped")
            )
        )
    )


def test_skipping_of_tests_missing_in_testplan(
    monkeypatch: MonkeyPatch,
    rst_examples: RstExampleTable,
    behave_runner: AllureBehaveRunner
):
    monkeypatch.setenv(
        "ALLURE_TESTPLAN_PATH",
        str(
            behave_runner.pytester.makefile(
                ".json",
                rst_examples["fullname-testplan"]
            )
        )
    )

    behave_runner.run_rst_example(
        "fullname-feature-1",
        "fullname-feature-2",
        steps=["steps"],
        cli_args=["-D", "AllureFormatter.hide_excluded=True"]
    )

    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario selection",
                with_status("passed")
            ),
            not_(
                has_test_case("Scenario deselection")
            ),
            has_test_case(
                "Scenario selection 2",
                with_status("passed")
            ),
            not_(
                has_test_case("Scenario deselection 2")
            )
        )
    )
