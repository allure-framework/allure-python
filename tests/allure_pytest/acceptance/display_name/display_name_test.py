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


def test_param_id_in_display_name(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.mark.parametrize("name", [pytest.param("value", id="some id")])
    ... @allure.title('Title with id - {param_id}')
    ... def test_param_id(name):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_param_id",
            has_title("Title with id - some id")
        )
    )


def test_no_param_id_in_display_name(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.mark.parametrize("param1, param2", [pytest.param("value1", "value2")])
    ... @allure.title('Title with id - {param_id}')
    ... def test_no_param_id(param1, param2):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_no_param_id",
            has_title("Title with id - value1-value2")
        )
    )


def test_non_ascii_id_in_display_name(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.mark.parametrize("name", [pytest.param("value", id="Ид,本我,पहचान,بطاقة تعريف")])
    ... @allure.title('Title with non-ASCII id - {param_id}')
    ... def test_non_ascii_param_id(name):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_non_ascii_param_id",
            has_title("Title with non-ASCII id - Ид,本我,पहचान,بطاقة تعريف")
        )
    )


def test_explicit_parameter_called_param_id_in_display_name(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import allure
    >>> import pytest

    >>> @pytest.mark.parametrize("param_id", [pytest.param("param value", id="some id")])
    ... @allure.title('Title with id - {param_id}')
    ... def test_explicit_parameter_called_param_id(param_id):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_explicit_parameter_called_param_id",
            has_title("Title with id - param value")
        )
    )
