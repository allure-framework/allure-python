from hamcrest import assert_that, not_
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.label import has_tag


def test_pytest_marker(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.cool
    ... @pytest.mark.stuff
    ... def test_pytest_marker_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_example",
            has_tag("cool"),
            has_tag("stuff")
        )
    )


def test_show_reserved_pytest_markers_full_decorator(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.usermark1
    ... @pytest.mark.usermark2
    ... @pytest.mark.parametrize("param", ["foo"])
    ... @pytest.mark.skipif(False, reason="reason2")
    ... @pytest.mark.skipif(False, reason="reason1")
    ... def test_show_reserved_pytest_markers_full_decorator_example(param):
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_show_reserved_pytest_markers_full_decorator_example[foo]",
            has_tag("usermark1"),
            has_tag("usermark2"),
            has_tag("@pytest.mark.skipif(False, reason='reason1')"),
            not_(
                has_tag("@pytest.mark.skipif(False, reason='reason2')")
            ),
            not_(
                has_tag("@pytest.mark.parametrize('param', ['foo'])")
            )
        )
    )


def test_pytest_xfail_marker(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.xfail(reason='this is unexpect pass')
    ... def test_pytest_xfail_marker_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_xfail_marker_example",
            has_tag("@pytest.mark.xfail(reason='this is unexpect pass')")
        )
    )


def test_pytest_marker_with_args(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.marker('cool', 'stuff')
    ... def test_pytest_marker_with_args_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_with_args_example",
            has_tag("marker('cool', 'stuff')")
        )
    )


def test_pytest_marker_with_kwargs(allure_pytest_runner: AllurePytestRunner):
    """
    >>> import pytest

    >>> @pytest.mark.marker(stuff='cool')
    ... def test_pytest_marker_with_kwargs_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_with_kwargs_example",
            has_tag("marker(stuff='cool')")
        )
    )


def test_pytest_marker_with_kwargs_native_encoding(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.marker(stuff='я')
    ... def test_pytest_marker_with_kwargs_native_encoding_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_with_kwargs_native_encoding_example",
            has_tag("marker(stuff='я')")
        )
    )


def test_pytest_marker_with_kwargs_utf_encoding(
    allure_pytest_runner: AllurePytestRunner
):
    """
    >>> import pytest

    >>> @pytest.mark.marker(stuff='я')
    ... def test_pytest_marker_with_kwargs_utf_encoding_example():
    ...     pass
    """

    allure_results = allure_pytest_runner.run_docstring()

    assert_that(
        allure_results,
        has_test_case(
            "test_pytest_marker_with_kwargs_utf_encoding_example",
            has_tag("marker(stuff='я')")
        )
    )
