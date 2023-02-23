from hamcrest import assert_that
from tests.allure_pytest.pytest_runner import AllurePytestRunner

from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link, has_issue_link


def test_link_pattern(allure_pytest_runner: AllurePytestRunner):
    """ ./allure-pytest/examples/link/dynamic_link.rst """

    allure_results = allure_pytest_runner.run_docpath_examples(
        "--allure-link-pattern",
        "issue:https://github.com/allure-framework/allure-python2/{}",
        "--allure-link-pattern",
        "docs:https://docs.qameta.io/{}"
    )

    assert_that(
        allure_results,
        has_test_case(
            "test_all_links_together",
            has_issue_link("https://github.com/allure-framework/allure-python2/issues/24"),
            has_issue_link("https://github.com/allure-framework/allure-python2/issues/24"),
            has_link("https://docs.qameta.io/allure")
        )
    )
