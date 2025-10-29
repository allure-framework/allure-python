import pytest
from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner
import allure

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title_path


@pytest.mark.parametrize(["path", "path_segments"], [
    pytest.param("foo.feature", ["Qux"], id="root"),
    pytest.param("foo/bar.feature", ["foo", "Qux"], id="dir"),
    pytest.param("foo/bar/baz.feature", ["foo", "bar", "Qux"], id="subdir"),
])
def test_title_path(allure_pytest_bdd_runner: AllurePytestRunner, path, path_segments):
    allure.dynamic.parent_suite("my suite")
    allure.dynamic.suite("my suite")
    allure.dynamic.sub_suite("my suite")

    allure.dynamic.epic("my suite")
    allure.dynamic.feature("my suite")
    allure.dynamic.story("my suite")

    feature_content = (
        """
        Feature: Qux
            Scenario: Quux
                Given pass
        """
    )
    pytest_content = (
        f"""
        from pytest_bdd import scenarios, given
        import allure

        scenarios("{path}")

        @given("pass")
        def given_pass():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        (path, feature_content),
        pytest_content,
    )

    assert_that(
        allure_results,
        has_test_case(
            "Quux",
            has_title_path(*path_segments),
        )
    )


def test_feature_name_missing(allure_pytest_bdd_runner: AllurePytestRunner):
    feature_content = (
        """
        Feature:
            Scenario: Bar
                Given pass
        """
    )
    pytest_content = (
        """
        from pytest_bdd import scenarios, given
        import allure

        scenarios("foo.feature")

        @given("pass")
        def given_pass():
            pass
        """
    )

    allure_results = allure_pytest_bdd_runner.run_pytest(
        ("foo.feature", feature_content),
        pytest_content,
        cli_args=["--capture=no"]
    )

    assert_that(
        allure_results,
        has_test_case(
            "Bar",
            has_title_path("foo.feature"),
        )
    )
