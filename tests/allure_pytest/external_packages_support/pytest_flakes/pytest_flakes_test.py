import allure
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import with_status


@allure.issue("352")
def test_pytest_flakes(allured_testdir):
    """
    >>> from os.path import *
    >>> def test_pytest_flakes_example():
    ...     assert True
    """

    allured_testdir.parse_docstring_source()
    allured_testdir.run_with_allure("--flakes")

    assert_that(allured_testdir.allure_report,
                has_test_case("flake-8",
                              with_status("broken")
                              ),

                )

    assert_that(allured_testdir.allure_report,
                has_test_case("test_pytest_flakes_example",
                              with_status("passed")
                              )

                )
