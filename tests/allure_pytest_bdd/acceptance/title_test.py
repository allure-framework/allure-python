from hamcrest import assert_that
from hamcrest import anything

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title
from allure_commons_test.result import has_step
from allure_commons_test.result import with_steps

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


def test_default_title_or_parametrized_test(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.parametrize("foo", ["bar"])
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
            has_title("Bar"),
        ),
    )


def test_step_title_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
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
            pass

        @allure.title("Lorem Ipsum")
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
            has_step("Lorem Ipsum"),
        ),
    )


def test_step_title_interpolation_step_args(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given the 'Lorem' string
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given, parsers
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @allure.title("{foo} Ipsum")
        @given(parsers.parse("the '{foo}' string"))
        def given_string(foo):
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
            has_step("Lorem Ipsum"),
        ),
    )


def test_step_title_interpolation_fixture(allure_pytest_bdd_runner: AllurePytestRunner):
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
        from pytest_bdd import scenario, given, then, parsers
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @pytest.fixture
        def foo():
            yield "Lorem Ipsum"

        @allure.title("{foo}")
        @given("noop")
        def given_noop(foo):
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
            has_step("Lorem Ipsum"),
        ),
    )


def test_step_title_interpolation_target_fixtures(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario: Bar
                Given a target fixture
                Then the value gets interpolated
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given, then, parsers
        import allure

        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("a target fixture", target_fixture="foo")
        def given_fixture():
            return "Lorem"

        @allure.title("{foo} Ipsum")
        @then("the value gets interpolated")
        def then_value_interpolated(foo):
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
                anything(),
                has_title("Lorem Ipsum"),
            ),
        ),
    )


def test_step_title_interpolation_pytest_params_explicit(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.parametrize("foo", ["Lorem"])
        @scenario("sample.feature", "Bar")
        def test_scenario(foo):
            pass

        @allure.title("{foo} Ipsum")
        @given("noop")
        def given_noop(foo):
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
            has_step("Lorem Ipsum"),
        ),
    )


def test_step_title_interpolation_pytest_params_implicit(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @pytest.mark.parametrize("foo", ["Lorem"])
        @scenario("sample.feature", "Bar")
        def test_scenario(foo):
            pass

        @allure.title("{foo} Ipsum")
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
            has_step("Lorem Ipsum"),
        ),
    )


def test_step_title_interpolation_outline_params(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario Outline: Bar
                Given noop

                Examples:
                | foo   | bar   |
                | Lorem | Ipsum |
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

        @allure.title("{foo} {bar}")
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
            has_step("Lorem Ipsum"),
        ),
    )


def test_step_title_interpolation_priority(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature: Foo
            Scenario Outline: Bar
                Given target fixture
                Then value 'Lorem Ipsum' received
                Then target fixture received
                Then outline param used
                Then pytest param used

                Examples:
                    | foo      | bar     |
                    | Outline  | Outline |
        """
    )
    steps_content = (
        """
        import pytest
        from pytest_bdd import scenario, given, then, parsers
        import allure

        @pytest.mark.parametrize(["foo", "bar"], [("Mark", "Mark")])
        @scenario("sample.feature", "Bar")
        def test_scenario(foo, bar):
            pass

        @given("target fixture", target_fixture="foo")
        def given_target_fixture():
            return "Target Fixture"

        @allure.title("{foo}")
        @then(parsers.parse("value '{foo}' received"))
        def then_value_received(foo):
            pass

        @allure.title("{foo}")
        @then("target fixture received")
        def then_target_fixture_received(foo):
            pass

        @allure.title("{foo}")
        @then("outline param used")
        def then_outline_param_used():
            pass

        @allure.title("{bar}")
        @then("pytest param used")
        def then_pytest_param_used(bar):
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
                anything(),
                has_title("Lorem Ipsum"),
                has_title("Target Fixture"),
                has_title("Outline"),
                has_title("Mark"),
            ),
        ),
    )
