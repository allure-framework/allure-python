""" ./allure-behave/examples/testplan.rst """

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from hamcrest import assert_that, all_of, not_
from tests.allure_behave.behave_runner import AllureBehaveRunner


def test_testplan_fullname_selection(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["fullname-feature-1", "fullname-feature-2"],
        step_rst_ids=["steps"],
        testplan_rst_id="fullname-testplan"
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


def test_testplan_id_selection(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["id-feature-1", "id-feature-2"],
        step_rst_ids=["steps"],
        testplan_rst_id="id-testplan"
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


def test_skipping_of_tests_missing_in_testplan(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["fullname-feature-1", "fullname-feature-2"],
        step_rst_ids=["steps"],
        testplan_rst_id="fullname-testplan",
        options=["-D", "AllureFormatter.hide_excluded=True"]
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
