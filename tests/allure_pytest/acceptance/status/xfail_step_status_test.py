from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_step
from allure_commons_test.result import with_status
from allure_commons_test.result import has_status_details
from allure_commons_test.result import with_message_contains
from allure_commons_test.result import with_trace_contains


def test_xfail_step_failure(executed_docstring_source):
    """
    >>> import pytest
    >>> import allure

    >>> @pytest.mark.xfail()
    ... def test_xfail_step_failure_example():
    ...     with allure.step("Step"):
    ...         assert False
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_xfail_step_failure_example",
                              with_status("skipped"),
                              has_status_details(with_message_contains("AssertionError"),
                                                 with_trace_contains("def test_xfail_step_failure_example():")
                                                 ),
                              has_step("Step",
                                       with_status("failed"),
                                       has_status_details(with_message_contains("AssertionError"),
                                                          with_trace_contains("test_xfail_step_failure_example")
                                                          )
                                       )
                              )
                )
