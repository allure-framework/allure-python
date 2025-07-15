from pathlib import Path
from hamcrest import assert_that
from tests.allure_behave.behave_runner import AllureBehaveRunner
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title_path


def test_titlepath_of_top_level_feature_file(docstring, behave_runner: AllureBehaveRunner):
    """
    Feature: Foo
    Scenario: Bar
        Given baz
    """

    behave_runner.run_behave(
        feature_files={"foo.feature": docstring},
        step_literals=["given('baz')(lambda c:None)"],
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Bar",
            has_title_path("Foo"),
        )
    )


def test_titlepath_of_nested_feature_file(docstring, behave_runner: AllureBehaveRunner):
    """
    Feature: Foo
    Scenario: Bar
        Given baz
    """

    behave_runner.run_behave(
        feature_files={"foo/bar/baz.feature": docstring},
        step_literals=["given('baz')(lambda c:None)"],
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Bar",
            has_title_path("foo", "bar", "Foo"),
        )
    )


def test_titlepath_if_feature_name_empty(docstring, behave_runner: AllureBehaveRunner):
    """
    Feature:
    Scenario: Bar
        Given baz
    """

    behave_runner.run_behave(
        feature_files={str(Path("foo.feature").absolute()): docstring},
        step_literals=["given('baz')(lambda c:None)"],
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Bar",
            has_title_path("foo.feature"),
        )
    )


def test_titlepath_of_feature_without_filename(docstring, behave_runner: AllureBehaveRunner):
    """
    Feature: Foo
    Scenario: Bar
        Given baz
    """

    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=["given('baz')(lambda c:None)"],
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Bar",
            has_title_path("Foo"),
        )
    )


def test_titlepath_of_feature_without_filename_and_name(docstring, behave_runner: AllureBehaveRunner):
    """
    Feature:
    Scenario: Bar
        Given baz
    """

    behave_runner.run_behave(
        feature_literals=[docstring],
        step_literals=["given('baz')(lambda c:None)"],
    )

    assert_that(
        behave_runner.allure_results,
        has_test_case(
            "Bar",
            has_title_path("Feature"),
        )
    )
