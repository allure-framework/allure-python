from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_history_id


def test_history_id(executed_docstring_source):
    """
    >>> def test_history_id_example():
    ...     assert True
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_history_id_example",
                              has_history_id()
                              )
                )


def test_history_id_for_skipped(executed_docstring_source):
    """
    >>> import pytest

    >>> @pytest.mark.skip
    ... def test_history_id_for_skipped_example():
    ...     assert True
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_history_id_for_skipped_example",
                              has_history_id()
                              )
                )
