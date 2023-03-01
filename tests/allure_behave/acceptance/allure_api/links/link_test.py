""" ./allure-behave/examples/link.rst """

from tests.allure_behave.behave_runner import AllureBehaveRunner
from hamcrest import assert_that, all_of
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_link
from allure_commons_test.result import has_issue_link
from allure_commons_test.result import has_test_case_link


def test_link_on_scenario_level(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["link-scenario-feature"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Scenario with the link to the allure report website",
            with_status("passed"),
            has_link("https://qameta.io/allure-report/", "link", "report")
        )
    )


def test_link_on_feature_level(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["link-feature-feature"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario with the link to the homepage",
                with_status("passed"),
                has_link("https://qameta.io", "link", "homepage")
            ),
            has_test_case(
                "Another scenario with the link to the homepage",
                with_status("passed"),
                has_link("https://qameta.io", "link", "homepage")
            )
        )
    )


def test_specialized_links(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["specialized-links-feature"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "Scenario associated with the issue",
                with_status("passed"),
                has_issue_link(
                    "https://github.com/allure-framework/allure-python/issues/1",
                    "https://github.com/allure-framework/allure-python/issues/1"
                )
            ),
            has_test_case(
                "Scenario associated with the TMS test case",
                with_status("passed"),
                has_test_case_link(
                    "https://qameta.io/#features",
                    "https://qameta.io/#features"
                )
            )
        )
    )


def test_dynamic_links(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["dynamic-links-feature"],
        step_rst_ids=["dynamic-links-steps"],
        environment_rst_id="dynamic-links-hooks"
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Issue from the step definition and link from the hook",
            with_status("passed"),
            has_issue_link(
                "https://github.com/allure-framework/allure-python/issues/1",
                "Skip None and empty values in json"
            ),
            has_link(
                "https://qameta.io/allure-report/",
                "link",
                "Allure Report"
            )
        )
    )
