""" ./allure-behave/examples/severity.rst """

import pytest
from tests.allure_behave.behave_runner import AllureBehaveRunner
from hamcrest import assert_that, all_of
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.label import has_severity


@pytest.mark.parametrize(["name", "sev"], [
    pytest.param("Blocking scenario", "blocker", id="blocker"),
    pytest.param("Critical scenario", "critical", id="critical"),
    pytest.param("Normal scenario", "normal", id="normal"),
    pytest.param("Minor scenario", "minor", id="minor"),
    pytest.param("Trivial scenario", "trivial", id="trivial")
])
def test_severity_on_scenario(name, sev, behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["severity-on-scenario"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        has_test_case(
            name,
            with_status("passed"),
            has_severity(sev)
        )
    )


def test_severity_on_feature(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["severity-on-feature"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "This scenario inherits the @cricial tag",
                with_status("passed"),
                has_severity("critical")
            ),
            has_test_case(
                "This scenario also inherits the @cricial tag",
                with_status("passed"),
                has_severity("critical")
            )
        )
    )


def test_multiple_severity_tags(behave_runner: AllureBehaveRunner):
    behave_runner.run_behave(
        feature_rst_ids=["multiple-severities"],
        step_literals=["given('noop')(lambda c:None)"]
    )
    assert_that(
        behave_runner.allure_results,
        all_of(
            has_test_case(
                "This is a trivial scenario",
                with_status("passed"),
                has_severity("trivial")
            ),
            has_test_case(
                "While this one is a blocker",
                with_status("passed"),
                has_severity("blocker")
            )
        )
    )
