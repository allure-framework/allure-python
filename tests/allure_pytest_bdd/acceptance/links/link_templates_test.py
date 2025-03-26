import pytest
from hamcrest import assert_that

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link
from allure_commons_test.result import has_issue_link

from tests.allure_pytest.pytest_runner import AllurePytestRunner


def test_decorator_link_formatted(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @allure.issue("726")
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
        cli_args=["--allure-link-pattern", "issue:https://github.com/allure-framework/allure-python/issues/{}"],
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_issue_link("https://github.com/allure-framework/allure-python/issues/726"),
        ),
    )


def test_dynamic_link_formatted(allure_pytest_bdd_runner: AllurePytestRunner):
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
            allure.dynamic.issue("726")

        @given("noop")
        def given_noop():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("sample.feature", feature_content),
        steps_content,
        cli_args=["--allure-link-pattern", "issue:https://github.com/allure-framework/allure-python/issues/{}"],
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_issue_link("https://github.com/allure-framework/allure-python/issues/726"),
        ),
    )


def test_type_mismatch_unchanged(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @allure.link("726", link_type="foo")
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
        cli_args=["--allure-link-pattern", "link:https://github.com/allure-framework/allure-python/issues/{}"],
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_link("726", link_type="foo"),
        ),
    )


def test_multiple_patterns_allowed(allure_pytest_bdd_runner: AllurePytestRunner):
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

        @allure.issue("726", name="issue-726")
        @allure.link("pytestbdd", link_type="framework", name="docs")
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
        cli_args=[
            "--allure-link-pattern",
            "framework:https://allurereport.org/docs/{}/",
            "--allure-link-pattern",
            "issue:https://github.com/allure-framework/allure-python/issues/{}",
        ],
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_issue_link("https://github.com/allure-framework/allure-python/issues/726", name="issue-726"),
            has_link("https://allurereport.org/docs/pytestbdd/", name="docs", link_type="framework"),
        ),
    )


@pytest.mark.parametrize("url", [
    "http://foo",
    "https://foo",
    "ftp://foo",
    "file:///foo",
    "customapp:custompath?foo=bar&baz=qux",
])
def test_full_urls_not_formatted(allure_pytest_bdd_runner: AllurePytestRunner, url):
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
        import allure

        @allure.link("{url}")
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
        cli_args=["--allure-link-pattern", "link:https://allurereport.org/{}/"],
    )

    assert_that(
        allure_results,
        has_test_case(
            "sample.feature:Bar",
            has_link(url),
        ),
    )
