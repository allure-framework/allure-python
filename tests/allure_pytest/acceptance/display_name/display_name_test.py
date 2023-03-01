""" ./allure-pytest/examples/display_name/display_name.rst"""

from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title
from allure_commons_test.label import has_label


def test_display_name(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_display_name",
            has_title("A some test title")
        )
    )


def test_display_name_template(allure_pytest_runner: AllurePytestRunner):
    allure_results = allure_pytest_runner.run_docpath_examples(cache=True)

    assert_that(
        allure_results,
        has_test_case(
            "test_display_name_template",
            has_title("A some test title with param False")
        )
    )


def test_fixture_value_in_display_name(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.fixture
    ... def fix():
    ...     return 'fixture value'

    >>> @allure.title('title with {fix}')
    ... def test_fixture_value_name(fix):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_value_name",
            has_title("title with fixture value")
        )
    )


def test_display_name_with_features(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @allure.feature('Feature 1')
    ... @allure.title('Titled test with features')
    ... @allure.feature('Feature 2')
    ... def test_feature_label_for_titled_test():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_feature_label_for_titled_test",
            has_label("feature", "Feature 1"),
            has_label("feature", "Feature 2"),
            has_title("Titled test with features")
        )
    )


def test_failed_fixture_value_in_display_name(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.fixture
    ... def fix():
    ...     raise AssertionError("Fixture failed for some reason")

    >>> @allure.title('title with {fix}')
    ... def test_fixture_value_name(fix):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_fixture_value_name",
            has_title("title with {fix}")
        )
    )
