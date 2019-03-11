# -*- coding: utf-8 -*-
""" ./examples/description/description.rst """

from hamcrest import assert_that, contains_string
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_description, has_description_html


def test_description(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_description",
                              has_description(contains_string("Test description"))
                              )
                )


def test_description_html(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_description_html",
                              has_description_html(contains_string("<h1>Html test description</h1>"))
                              )
                )


def test_docstring_description(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_docstring_description",
                              has_description(contains_string("Docstring"))
                              )
                )


def test_unicode_docstring_description(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_unicode_docstring_description",
                              has_description(contains_string("Докстринг в юникоде"))
                              )
                )
