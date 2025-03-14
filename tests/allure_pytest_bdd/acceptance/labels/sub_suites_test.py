from hamcrest import assert_that

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_sub_suite

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_sub_suite_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.sub_suite("Lorem Ipsum")
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
            has_sub_suite("Lorem Ipsum"),
        )
    )


def test_dynamic_sub_suite(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.sub_suite("Lorem Ipsum")

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
            has_sub_suite("Lorem Ipsum"),
        )
    )
