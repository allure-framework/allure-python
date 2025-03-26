from hamcrest import assert_that
from hamcrest import equal_to
from hamcrest import all_of
from hamcrest import has_entry
from hamcrest import contains_inanyorder

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_label

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_default_labels(allure_pytest_bdd_runner: AllurePytestRunner):
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
            has_entry(
                "labels",
                contains_inanyorder(
                    has_entry("name", "host"),
                    has_entry("name", "thread"),
                    all_of(
                        has_entry("name", "framework"),
                        has_entry("value", "pytest-bdd"),
                    ),
                    has_entry("name", "language"),
                    all_of(
                        has_entry("name", "feature"),
                        has_entry("value", "Foo"),
                    ),
                ),
            ),
        )
    )


def test_label_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @allure.label("foo", "bar", "baz")
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
            all_of(
                has_label("foo", equal_to("bar")),
                has_label("foo", equal_to("baz")),
            ),

        )
    )


def test_label_decorator_at_module_level(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenarios, given
        import allure

        pytestmark = [allure.label("foo", "bar", "baz")]

        scenarios("sample.feature")

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
            all_of(
                has_label("foo", equal_to("bar")),
                has_label("foo", equal_to("baz")),
            ),

        )
    )


def test_dynamic_label(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.label("foo", "bar", "baz")

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
            all_of(
                has_label("foo", equal_to("bar")),
                has_label("foo", equal_to("baz")),
            )
        )
    )
