from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_skip_in_step(executed_docstring_source):
    """
    >>> import pytest
    >>> import allure

    >>> def test_skip_in_step_example():
    ...     with allure.step("Step"):
    ...         pytest.skip()
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_skip_in_step_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("Skipped: <Skipped instance>")),
                              has_step("Step",
                                       with_status("skipped"),
                                       has_status_details(with_message_contains("Skipped: <Skipped instance>"),
                                                          with_trace_contains("test_skip_in_step")
                                                          )
                                       )
                              )
                )
