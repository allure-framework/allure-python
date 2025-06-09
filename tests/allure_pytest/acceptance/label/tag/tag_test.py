from hamcrest import assert_that, not_, anything
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_tag


def test_pytest_simple_markers_are_converted_to_allure_tags(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.cool
    ... @pytest.mark.stuff
    ... def test_pytest_simple_markers_are_converted_to_allure_tags_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_simple_markers_are_converted_to_allure_tags_example",
            has_tag("cool"),
            has_tag("stuff")
        )
    )


def test_pytest_marker_with_args_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.marker('cool', 'stuff')
    ... def test_pytest_marker_with_args_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_with_args_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_marker_with_kwargs_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.marker(stuff='cool')
    ... def test_pytest_marker_with_kwargs_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_with_kwargs_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_reserved_marker_usefixtures_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.usefixtures('test_fixture')
    ... def test_pytest_reserved_marker_usefixtures_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_reserved_marker_usefixtures_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_reserved_marker_filterwarnings_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.filterwarnings('ignore:val')
    ... def test_pytest_reserved_marker_filterwarnings_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_reserved_marker_filterwarnings_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_reserved_marker_skip_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.skip(reason='reason')
    ... def test_pytest_reserved_marker_skip_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_reserved_marker_skip_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_reserved_marker_skipif_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.skipif(False, reason='reason')
    ... def test_pytest_reserved_marker_skipif_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_reserved_marker_skipif_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_reserved_marker_xfail_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(reason='this is unexpect pass')
    ... def test_pytest_reserved_marker_xfail_is_not_converted_to_allure_tag_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_reserved_marker_xfail_is_not_converted_to_allure_tag_example",
            not_(
                has_tag(anything())
            )
        )
    )


def test_pytest_reserved_marker_parametrize_is_not_converted_to_allure_tag(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.parametrize("param", ["foo"])
    ... def test_pytest_reserved_marker_parametrize_is_not_converted_to_allure_tag_example(param):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_reserved_marker_parametrize_is_not_converted_to_allure_tag_example[foo]",
            not_(
                has_tag(anything())
            )
        )
    )
