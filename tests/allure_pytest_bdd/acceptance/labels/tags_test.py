import pytest

from hamcrest import assert_that
from hamcrest import not_
from hamcrest import all_of

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_tag

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_tag_decorator(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @allure.tag("foo", "bar")
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
            has_tag("foo"),
            has_tag("bar"),
        )
    )


def test_dynamic_tag(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.tag("foo", "bar")

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
            has_tag("foo"),
            has_tag("bar"),
        )
    )


def test_pytest_mark_reported(allure_pytest_bdd_runner: AllurePytestRunner):
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
        import pytest

        @pytest.mark.foo
        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )
    conftest_content = (
        """
        def pytest_configure(config):
            config.addinivalue_line("markers", f"foo: lorem ipsum")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        conftest_literal=conftest_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_tag("foo"),
        )
    )


def test_pytest_marks_with_arg_not_reported(allure_pytest_bdd_runner: AllurePytestRunner):
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
        import pytest

        @pytest.mark.foo("bar")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )
    conftest_content = (
        """
        def pytest_configure(config):
            config.addinivalue_line("markers", f"foo: lorem ipsum")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        conftest_literal=conftest_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            not_(has_tag("foo")),
        )
    )


def test_pytest_marks_with_kwarg_not_reported(allure_pytest_bdd_runner: AllurePytestRunner):
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
        import pytest

        @pytest.mark.foo(foo="bar")
        @scenario("sample.feature", "Bar")
        def test_scenario():
            pass

        @given("noop")
        def given_noop():
            pass
        """
    )
    conftest_content = (
        """
        def pytest_configure(config):
            config.addinivalue_line("markers", f"foo: lorem ipsum")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        conftest_literal=conftest_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            not_(has_tag("foo")),
        )
    )


# Can't check argless skip/skipif: skipepd tests currently not reported
@pytest.mark.parametrize("mark", ["usefixtures", "filterwarnings", "xfail"])
def test_builtin_pytest_marks_not_reported(allure_pytest_bdd_runner: AllurePytestRunner, mark):
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
        import pytest

        @pytest.mark.{mark}
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
            not_(has_tag(mark)),
        )
    )


def test_parametrize_mark_not_reported(allure_pytest_bdd_runner: AllurePytestRunner):
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
        import pytest

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
            not_(has_tag("parametrize")),
        )
    )


def test_skipif_mark_not_reported(allure_pytest_bdd_runner: AllurePytestRunner):
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
        import pytest

        @pytest.mark.skipif(False, reason="Lorem Ipsum")
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
            not_(has_tag("skipif")),
        )
    )


def test_gherkin_tags_reported(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        @foo
        Feature: Foo
            @bar
            Scenario: Bar
                Given noop

            @baz
            Scenario: Baz
                Given noop
        """
    )
    steps_content = (
        """
        from pytest_bdd import scenarios, given
        import pytest

        scenarios("sample.feature")

        @given("noop")
        def given_noop():
            pass
        """
    )
    conftest_content = (
        """
        def pytest_configure(config):
            config.addinivalue_line("markers", f"foo: foo")
            config.addinivalue_line("markers", f"bar: bar")
            config.addinivalue_line("markers", f"baz: baz")
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        conftest_literal=conftest_content,
    )

    assert_that(
        allure_results,
        all_of(
            has_test_case(
                "sample.feature:Bar",
                has_tag("foo"),
                has_tag("bar"),
            ),
            has_test_case(
                "sample.feature:Baz",
                has_tag("foo"),
                has_tag("baz"),
            ),
        ),
    )
