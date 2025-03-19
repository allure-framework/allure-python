from hamcrest import assert_that
from hamcrest import not_
from hamcrest import empty
from hamcrest import all_of
from hamcrest import has_entry
from hamcrest import anything

from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_passed_scenario(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with_status("passed"),
            not_(has_status_details()),
        ),
    )


def test_scenario_fail_in_step(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with_status("failed"),
            has_status_details(
                with_message_contains("AssertionError: assert False"),
                with_trace_contains("def given_fail():"),
            ),
        ),
    )


def test_scenario_fail_in_scenario(allure_pytest_bdd_runner: AllurePytestRunner):
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
            assert False

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
            with_status("failed"),
            has_status_details(
                with_message_contains("AssertionError: assert False"),
                with_trace_contains("def test_scenario():"),
            ),
        ),
    )


def test_scenario_break_in_step(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with_status("broken"),
            has_status_details(
                with_message_contains("ValueError: Lorem Ipsum"),
                with_trace_contains("def given_break():"),
            ),
        ),
    )


def test_scenario_break_in_scenario(allure_pytest_bdd_runner: AllurePytestRunner):
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
            raise ValueError("Lorem Ipsum")

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
            with_status("broken"),
            has_status_details(
                with_message_contains("ValueError: Lorem Ipsum"),
                with_trace_contains("def test_scenario():"),
            ),
        ),
    )


def test_scenario_skip_in_step(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with_status("skipped"),
            has_status_details(
                with_message_contains("Skipped: Lorem Ipsum"),
                with_trace_contains("test_scenario_skip_in_step.py"),
            ),
        ),
    )


def test_scenario_skip_in_scenario(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pytest.skip("Lorem Ipsum")

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
            with_status("skipped"),
            has_status_details(
                with_message_contains("Skipped: Lorem Ipsum"),
                with_trace_contains("test_scenario_skip_in_scenario.py"),
            ),
        ),
    )


def test_scenario_skip_mark(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.skip("Lorem Ipsum")
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

    assert_that(allure_results.test_cases, empty())


def test_scenario_xfail_in_step(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with_status("skipped"),
            has_status_details(
                all_of(
                    with_message_contains("XFailed: Lorem Ipsum"),
                    not_(with_message_contains("XFAIL reason: Lorem Ipsum\n\n")),
                ),
                with_trace_contains("def given_xfail():"),
            ),
        ),
    )


def test_scenario_xfail_in_scenario(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pytest.xfail("Lorem Ipsum")

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
            with_status("skipped"),
            has_status_details(
                all_of(
                    with_message_contains("XFailed: Lorem Ipsum"),
                    not_(with_message_contains("XFAIL reason: Lorem Ipsum\n\n")),
                ),
                with_trace_contains("def test_scenario():"),
            ),
        ),
    )


def test_scenario_xfail_mark(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.xfail(reason="Lorem Ipsum")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            assert False

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
            with_status("skipped"),
            has_status_details(
                with_message_contains("XFAIL Lorem Ipsum\n\nAssertionError: assert False"),
                with_trace_contains("def test_scenario():"),
            ),
        ),
    )


def test_scenario_xfail_mark_passed(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.xfail(reason="Lorem Ipsum")
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
            with_status("passed"),
            has_status_details(
                with_message_contains("XPASS Lorem Ipsum"),
                not_(has_entry("trace", anything())),
            ),
        ),
    )

def test_scenario_xfail_mark_strict(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.xfail(reason="Lorem Ipsum", strict=True)
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
            with_status("broken"),
            has_status_details(
                with_message_contains("[XPASS(strict)] Lorem Ipsum"),
                not_(has_entry("trace", anything())),
            ),
        ),
    )


def test_passed_setup_teardown(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.fixture
        def setup():
            yield

        @scenario("sample.feature", "Bar")
        def test_scenario(setup):
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
            with_status("passed"),
            not_(has_status_details()),
        ),
    )


def test_passed_teardown_not_overwrite_failed_status(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.fixture
        def setup():
            yield

        @scenario("sample.feature", "Bar")
        def test_scenario(setup):
            assert False

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
            with_status("failed"),
        ),
    )


def test_failed_teardown_overwrite_passed_status(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.fixture
        def setup():
            yield
            assert False

        @scenario("sample.feature", "Bar")
        def test_scenario(setup):
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
            with_status("failed"),
        ),
    )


def test_broken_teardown_overwrite_passed_status(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.fixture
        def setup():
            yield
            raise ValueError("Lorem Ipsum")

        @scenario("sample.feature", "Bar")
        def test_scenario(setup):
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
            with_status("broken"),
        ),
    )


def test_skipped_teardown_not_overwrite_passed_status(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.fixture
        def setup():
            yield
            pytest.skip("Lorem Ipsum")

        @scenario("sample.feature", "Bar")
        def test_scenario(setup):
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
            with_status("passed"),
        ),
    )
