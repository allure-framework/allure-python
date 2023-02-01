from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains


def test_skip(executed_docstring_source):
    """
    >>> import pytest

    >>> def test_skip_example():
    ...     pytest.skip()
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skip_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("Skipped"))
                              )
                )


def test_skip_with_reason(executed_docstring_source):
    """
    >>> import pytest

    >>> def test_skip_with_reason_example():
    ...     pytest.skip("Skip reason")
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skip_with_reason_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("Skipped: Skip reason"))
                              )
                )


def test_skip_decorator_and_reason(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.skip(reason="Skip reason")
    ... def test_skip_decorator_and_reason_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skip_decorator_and_reason_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("Skipped: Skip reason"))
                              )
                )


def test_skipif_true(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.skipif(True, reason="Skip reason")
    ... def test_skipif_true_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skipif_true_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("Skipped: Skip reason"))
                              )
                )


def test_skipif_false(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.skipif(False, reason="Skip reason")
    ... def test_skipif_false_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skipif_false_example",
                              with_status("passed")
                              )
                )
