from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link, has_issue_link


def test_link_pattern(allured_testdir):
    """ ./examples/link/dynamic_link.rst """

    allured_testdir.parse_docstring_path()

    allured_testdir.run_with_allure("--allure-link-pattern",
                                    "issue:https://github.com/allure-framework/allure-python2/{}",
                                    "--allure-link-pattern",
                                    "docs:https://docs.qameta.io/{}")

    assert_that(allured_testdir.allure_report,
                has_test_case("test_all_links_together",
                              has_issue_link("https://github.com/allure-framework/allure-python2/issues/24"),
                              has_issue_link("https://github.com/allure-framework/allure-python2/issues/24"),
                              has_link("https://docs.qameta.io/allure")
                              )
                )
