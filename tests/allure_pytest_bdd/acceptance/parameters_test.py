from hamcrest import assert_that
from hamcrest import all_of
from hamcrest import equal_to
from hamcrest import not_
from hamcrest import has_length

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_parameter
from allure_commons_test.result import with_mode
from allure_commons_test.result import with_excluded
from allure_commons_test.result import has_history_id

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_parameter_added(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.parameter("foo", "bar")

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
            has_parameter("foo", "'bar'"),
        ),
    )


def test_masked_parameter(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.parameter("foo", "bar", mode=allure.parameter_mode.MASKED)

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
            has_parameter("foo", "'bar'", with_mode("masked")),
        ),
    )


def test_hidden_parameter(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.parameter("foo", "bar", mode=allure.parameter_mode.HIDDEN)

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
            has_parameter("foo", "'bar'", with_mode("hidden")),
        ),
    )


def test_excluded_parameter(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.parameter("foo", "bar", excluded=True)

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
            has_parameter("foo", "'bar'", with_excluded()),
        ),
    )


def test_parameters_affect_history_id(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    impl_with_no_parameter = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )
    impl_with_parameter = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.parameter("foo", "bar")

        @given("noop")
        def given_noop():
            pass
        """
    )

    results_with_no_parameter = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        impl_with_no_parameter,
    )

    results_with_parameter = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        impl_with_parameter,
    )

    assert_that(
        results_with_parameter,
        has_test_case(
            "sample.feature:Bar",
            has_history_id(
                not_(equal_to(results_with_no_parameter.test_cases[0]["historyId"])),
            ),
        ),
    )


def test_parameters_order_doesnt_matter(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    impl_order1 = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.parameter("baz", "qux")
            allure.dynamic.parameter("foo", "bar")

        @given("noop")
        def given_noop():
            pass
        """
    )
    impl_order2 = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.parameter("foo", "bar")
            allure.dynamic.parameter("baz", "qux")

        @given("noop")
        def given_noop():
            pass
        """
    )

    results_order1 = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        impl_order1,
    )

    results_order2 = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        impl_order2,
    )

    assert_that(
        results_order1,
        has_test_case(
            "sample.feature:Bar",
            has_history_id(
                equal_to(results_order2.test_cases[0]["historyId"]),
            ),
        ),
    )


def test_excluded_parameters_doesnt_affect_history_id(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    impl_no_parameter = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )
    impl_excluded_parameter = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            allure.dynamic.parameter("foo", "bar", excluded=True)

        @given("noop")
        def given_noop():
            pass
        """
    )

    results_no_parameter = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        impl_no_parameter,
    )

    results_excluded_parameter = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        impl_excluded_parameter,
    )

    assert_that(
        results_no_parameter,
        has_test_case(
            "sample.feature:Bar",
            has_history_id(
                equal_to(results_excluded_parameter.test_cases[0]["historyId"]),
            ),
        ),
    )


def test_pytest_parameters_added(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    impl_content = (
        """
        import pytest
        from pytest_bdd import scenario, given

        @pytest.mark.parametrize("foo", ["bar", {"baz": "qux"}])
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
        impl_content,
    )

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "sample.feature:Bar",
                has_parameter("foo", "'bar'"),
            ),
            has_test_case(
                "sample.feature:Bar",
                has_parameter("foo", "{'baz': 'qux'}"),
            ),
        ),
    )


def test_original_pytest_parameter_values_used_to_get_history_id(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given noop
        """
    )
    impl_content = (
        """
        import pytest
        from pytest_bdd import scenario, given

        @pytest.mark.parametrize("foo", [b"bar", b"baz"])
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
        impl_content,
    )

    history_ids = {tc["historyId"] for tc in allure_results.test_cases}

    assert_that(history_ids, has_length(2))
