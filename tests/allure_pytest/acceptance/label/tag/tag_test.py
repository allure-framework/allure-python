from hamcrest import assert_that, not_
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
                has_tag("marker('cool', 'stuff')")
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
                has_tag("marker(stuff='cool')")
            )
        )
    )


def test_pytest_multiple_simple_and_reserved_markers_to_allure_tags(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.usermark1
    ... @pytest.mark.usermark2
    ... @pytest.mark.parametrize("param", ["foo"])
    ... @pytest.mark.skipif(False, reason="reason2")
    ... @pytest.mark.skipif(False, reason="reason1")
    ... def test_pytest_multiple_simple_and_reserved_markers_to_allure_tags_example(param):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_multiple_simple_and_reserved_markers_to_allure_tags_example[foo]",
            has_tag("usermark1"),
            has_tag("usermark2"),
            not_(
                has_tag("skipif(False, reason='reason1')")
            ),
            not_(
                has_tag("skipif(False, reason='reason2')")
            ),
            not_(
                has_tag("parametrize('param', ['foo'])")
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
                has_tag("usefixtures('test_fixture')")
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
                has_tag("filterwarnings('ignore:val')")
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
                has_tag("skip(reason='reason')")
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
                has_tag("skipif(False, reason='reason')")
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
                has_tag("xfail(reason='this is unexpect pass')")
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
                has_tag("parametrize('param', ['foo'])")
            )
        )
    )


def test_pytest_simple_markers_utf_encoding_are_converted_to_allure_tags(
        allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.классная
    >>> @pytest.mark.штука
    ... def test_pytest_simple_markers_utf_encoding_are_converted_to_allure_tags_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_simple_markers_utf_encoding_are_converted_to_allure_tags_example",
            has_tag("классная"),
            has_tag("штука")
        )
    )
