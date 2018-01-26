# -*- coding: utf-8 -*-
import pytest
import allure


@allure.title("A some test title")
def test_display_name():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_display_name',
    ...                           has_title("A some test title")
    ...             )
    ... )
    """


@allure.title("A some test title with param {param}")
@pytest.mark.parametrize('param', [False])
def test_display_name_template(param):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_display_name_template[False]',
    ...                           has_title("A some test title with param False")
    ...             )
    ... )
    """
    assert param


@allure.title(u"Тест с шаблоном и параметром: {param}")
@pytest.mark.parametrize('param', [False])
def test_unicode_display_name_template(param):
    u"""
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_unicode_display_name_template[False]',
    ...                           has_title(u"Тест с шаблоном и параметром: False")
    ...             )
    ... )
    """
    assert param


@allure.title(u"Лунтик")
def test_unicode_display_name():
    u"""
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_unicode_display_name',
    ...                           has_title(u"Лунтик")
    ...             )
    ... )
    """