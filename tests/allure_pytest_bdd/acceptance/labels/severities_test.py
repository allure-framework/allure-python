import pytest
from hamcrest import assert_that

import allure

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_severity

from tests.allure_pytest.pytest_runner import AllurePytestRunner


@pytest.mark.parametrize("severity", allure.severity_level)
def test_severity_decorator(allure_pytest_bdd_runner: AllurePytestRunner, severity):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        f"""
        from pytest_bdd import scenario, given
        import allure

        @allure.severity(allure.severity_level.{severity.name})
        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_severity(severity.value),
        )
    )


@pytest.mark.parametrize("severity", allure.severity_level)
def test_dynamic_severity(allure_pytest_bdd_runner: AllurePytestRunner, severity):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        f"""
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.severity(allure.severity_level.{severity.name})

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_severity(severity.value),
        )
    )
