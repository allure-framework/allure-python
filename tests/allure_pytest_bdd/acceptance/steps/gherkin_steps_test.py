from hamcrest import assert_that
from hamcrest import not_
from hamcrest import all_of

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title
from allure_commons_test.result import has_step
from allure_commons_test.result import with_steps
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_passed_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given pass
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("pass")
        def given_pass():
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
            has_step(
                "Given pass",
                with_status("passed"),
                not_(has_status_details()),
            ),
        ),
    )


def test_failed_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given fail
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("fail")
        def given_fail():
            assert False
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
            has_step(
                "Given fail",
                with_status("failed"),
                has_status_details(
                    with_message_contains("AssertionError: assert False"),
                    with_trace_contains("in given_fail"),
                ),
            ),
        ),
    )


def test_broken_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given break
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("break")
        def given_break():
            raise ValueError("Lorem Ipsum")
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
            has_step(
                "Given break",
                with_status("broken"),
                has_status_details(
                    with_message_contains("ValueError: Lorem Ipsum"),
                    with_trace_contains("in given_break"),
                ),
            ),
        ),
    )


def test_skipped_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given skip
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("skip")
        def given_skip():
            pytest.skip("Lorem Ipsum")
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
            has_step(
                "Given skip",
                with_status("skipped"),
                has_status_details(
                    with_message_contains("Skipped: Lorem Ipsum"),
                    with_trace_contains("in given_skip"),
                ),
            ),
        ),
    )


def test_xfailed_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given xfail
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("xfail")
        def given_xfail():
            pytest.xfail("Lorem Ipsum")
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
            has_step(
                "Given xfail",
                with_status("skipped"),
                has_status_details(
                    with_message_contains("XFailed: Lorem Ipsum"),
                    with_trace_contains("in given_xfail"),
                ),
            ),
        ),
    )


def test_remaining_steps_are_reported_after_failed(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given fail
                When skip
                Then skip
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given, when, then
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("fail")
        def given_fail():
            assert False

        @when("skip")
        def when_skip():
            pass

        @then("skip")
        def then_skip():
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
            with_steps(
                has_title("Given fail"),
                all_of(
                    has_title("When skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
                all_of(
                    has_title("Then skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
            ),
        ),
    )


def test_remaining_steps_are_reported_after_skipped(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given skip
                When skip
                Then skip
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given, when, then
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("skip")
        def given_skip():
            pytest.skip("Lorem Ipsum")

        @when("skip")
        def when_skip():
            pass

        @then("skip")
        def then_skip():
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
            with_steps(
                has_title("Given skip"),
                all_of(
                    has_title("When skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
                all_of(
                    has_title("Then skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
            ),
        ),
    )


def test_remaining_steps_are_reported_after_xfailed(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given xfail
                When skip
                Then skip
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given, when, then
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("xfail")
        def given_xfail():
            pytest.xfail("Lorem Ipsum")

        @when("skip")
        def when_skip():
            pass

        @then("skip")
        def then_skip():
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
            with_steps(
                has_title("Given xfail"),
                all_of(
                    has_title("When skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
                all_of(
                    has_title("Then skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
            ),
        ),
    )


def test_undefined_step(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given unknown
                When skip
                Then skip
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given, when, then
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @when("skip")
        def when_skip():
            pass

        @then("skip")
        def then_skip():
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
            with_steps(
                all_of(
                    has_title("Given unknown"),
                    with_status("broken"),
                    has_status_details(
                        with_message_contains("Step definition is not found: Given \"unknown\""),
                    ),
                ),
                all_of(
                    has_title("When skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
                all_of(
                    has_title("Then skip"),
                    with_status("skipped"),
                    not_(has_status_details()),
                ),
            ),
        ),
    )
