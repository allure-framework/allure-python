""" ./examples/link/link.rst """

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link
from allure_commons_test.result import has_issue_link
from allure_commons_test.result import has_test_case_link


def test_link(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_link",
                              has_link("http://qameta.io")
                              )
                )


def test_issue_link(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_issue_link",
                              has_issue_link("https://github.com/allure-framework/allure-python/issues/24")
                              )
                )


def test_testcase_link(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_testcase_link",
                              has_test_case_link("issues/24#issuecomment-277330977")
                              )
                )


def test_custom_link(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_custom_link",
                              has_link("http://qameta.io", name="QAMETA", link_type="homepage")
                              )
                )
