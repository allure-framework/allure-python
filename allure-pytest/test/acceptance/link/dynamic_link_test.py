""" ./examples/link/dynamic_link.rst """

import pytest
from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_link, has_issue_link, has_test_case_link


def test_dynamic_link(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_dynamic_link",
                              has_issue_link("issues/24")
                              )
                )


@pytest.mark.parametrize('link', ["issues/24", "issues/132"])
def test_parametrize_dynamic_link(executed_docstring_path, link):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_parametrize_dynamic_link[{link}]".format(link=link),
                              has_issue_link(link),
                              )
                )


def test_all_links_together(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_all_links_together",
                              has_issue_link("issues/24"),
                              has_issue_link("issues/24"),
                              has_link("allure", name="QAMETA", link_type="docs")
                              )
                )
