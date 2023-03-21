"""./examples/description/dynamic_description.rst"""

from hamcrest import assert_that, contains_string
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description, has_description_html


def test_dynamic_description(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_dynamic_description",
                              has_description(contains_string("Actual description"))
                              )
                )


def test_dynamic_description_html(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_dynamic_description_html",
                              has_description_html(contains_string("<p>Actual HTML description</p>"))
                              )
                )
