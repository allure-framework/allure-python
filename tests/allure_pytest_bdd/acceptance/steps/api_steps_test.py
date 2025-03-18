from hamcrest import assert_that
from hamcrest import all_of

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title
from allure_commons_test.result import has_step
from allure_commons_test.result import with_steps
from allure_commons_test.result import with_status
from allure_commons_test.result import has_parameter
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_one_context_substep(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given substep
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("substep")
        def given_substep():
            with allure.step("foo"):
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
                "Given substep",
                has_step(
                    "foo",
                    with_status("passed"),
                ),
            ),
        ),
    )


def test_one_function_substep(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given substep
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.step("foo")
        def fn():
            pass

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("substep")
        def given_substep():
            fn()
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
                "Given substep",
                has_step(
                    "foo",
                    with_status("passed"),
                ),
            ),
        ),
    )


def test_nested_substeps(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given substeps
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenario, given
        import allure

        @allure.step("foo")
        def fn():
            pass

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("substeps")
        def given_substeps():
            with allure.step("1"):
                with allure.step("1.1"):
                    pass
                with allure.step("1.2"):
                    pass
            with allure.step("2"):
                with allure.step("2.1"):
                    pass
                with allure.step("2.2"):
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
                "Given substeps",
                with_steps(
                    all_of(
                        has_title("1"),
                        with_status("passed"),
                        with_steps(
                            all_of(
                                has_title("1.1"),
                                with_status("passed"),
                            ),
                            all_of(
                                has_title("1.2"),
                                with_status("passed"),
                            ),
                        ),
                    ),
                    all_of(
                        has_title("2"),
                        with_status("passed"),
                        with_steps(
                            all_of(
                                has_title("2.1"),
                                with_status("passed"),
                            ),
                            all_of(
                                has_title("2.2"),
                                with_status("passed"),
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )


def test_substep_with_parameters(allure_pytest_bdd_runner: AllurePytestRunner):
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
            pass

        @given("noop")
        def given_noop():
            step = allure.step("foo")
            step.params = {"foo": "bar", "baz": {"qux": "qut"}}
            with step:
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
                "Given noop",
                has_step(
                    "foo",
                    with_status("passed"),
                    has_parameter("foo", "'bar'"),
                    has_parameter("baz", "{'qux': 'qut'}"),
                ),
            ),
        ),
    )


def test_failed_substep(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with allure.step("foo"):
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
                has_step(
                    "foo",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("AssertionError: assert False"),
                        with_trace_contains("in given_fail"),
                    ),
                ),
            ),
        ),
    )


def test_broken_substep(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with allure.step("foo"):
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
                has_step(
                    "foo",
                    with_status("broken"),
                    has_status_details(
                        with_message_contains("ValueError: Lorem Ipsum"),
                        with_trace_contains("in given_break"),
                    ),
                ),
            ),
        ),
    )


def test_skipped_substep(allure_pytest_bdd_runner: AllurePytestRunner):
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
            with allure.step("foo"):
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
                has_step(
                    "foo",
                    with_status("skipped"),
                    has_status_details(
                        with_message_contains("Skipped: Lorem Ipsum"),
                        with_trace_contains("in given_skip"),
                    ),
                ),
            ),
        ),
    )
