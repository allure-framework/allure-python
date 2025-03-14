from hamcrest import assert_that

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
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
                "Given noop",
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
                Given noop
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

        @given("noop")
        def given_noop():
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
                "Given noop",
                has_step(
                    "foo",
                    with_status("passed"),
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
                "Given noop",
                has_step(
                    "foo",
                    with_status("failed"),
                    has_status_details(
                        with_message_contains("AssertionError: assert False"),
                        with_trace_contains("in given_noop"),
                    ),
                ),
            ),
        ),
    )
