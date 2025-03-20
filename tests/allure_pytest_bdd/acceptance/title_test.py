from hamcrest import assert_that

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_title_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @allure.title("Lorem Ipsum")
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
            has_title("Lorem Ipsum"),
        ),
    )


def test_title_interpolations(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario Outline: Bar
                Given noop

                Examples:
                    | bar   |
                    | Ipsum |
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given
        import allure

        @allure.title("{foo} {bar}")
        @pytest.mark.parametrize("foo", ["Lorem"])
        @scenario("sample.feature", "Bar")
        def test_scenario(foo):
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
            has_title("Lorem Ipsum"),
        ),
    )


def test_dynamic_title(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given
        import allure

        @allure.title("This will be overwritten")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.title("Lorem Ipsum")

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
            has_title("Lorem Ipsum"),
        ),
    )
