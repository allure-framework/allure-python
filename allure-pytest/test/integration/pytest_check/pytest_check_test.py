
import allure
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status, with_message_contains, has_status_details
from hamcrest import assert_that


@allure.issue("376")
@allure.feature("Integration")
def test_pytest_check(allured_testdir):
    """
    >>> import pytest_check as check
    >>> def test_pytest_check_example():
    ...     check.equal(1, 2, msg="First failure")
    ...     check.equal(1, 2, msg="Second failure")
    """

    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure()

    assert_that(allured_testdir.allure_report,
                has_test_case("test_pytest_check_example",
                              with_status("failed"),
                              has_status_details(with_message_contains("First failure"),
                                                 with_message_contains("Second failure"))
                              ),

                )
