# -*- coding: utf-8 -*-
""" ./examples/display_name/display_name.rst"""

from hamcrest import assert_that
from allure_commons_test.report import has_test_case
from allure_commons_test.result import has_title


def test_display_name(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_display_name",
                              has_title("A some test title")
                              )
                )


def test_display_name_template(executed_docstring_path):
    assert_that(executed_docstring_path.allure_report,
                has_test_case("test_display_name_template",
                              has_title("A some test title with param False")
                              )
                )


def test_unicode_display_name(executed_docstring_source):
    """
    >>> import allure

    >>> @allure.title(u"Лунтик")
    >>> def test_unicode_display_name_example():
    ...     pass
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_unicode_display_name_example", has_title(u"Лунтик"))
                )


def test_unicode_display_name_template(executed_docstring_source):
    """
    >>> import allure
    >>> import pytest

    >>> @allure.title(u"Тест с шаблоном и параметром: {param}")
    ... @pytest.mark.parametrize("param", [False])
    ... def test_unicode_display_name_template_example(param):
    ...     assert param
    """

    assert_that(executed_docstring_source.allure_report,
                has_test_case("test_unicode_display_name_template_example",
                              has_title(u"Тест с шаблоном и параметром: False")
                              )
                )
