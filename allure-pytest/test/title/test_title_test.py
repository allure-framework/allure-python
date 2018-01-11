# -*- coding: utf-8 -*-
import allure


@allure.title("A some test tile")
def test_title():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_title',
    ...                           has_title("A some test tile")
    ...             )
    ... )
    """
    pass


@allure.title(u"Лунтик")
def test_unicode_title():
    u"""
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_unicode_title',
    ...                           has_title(u"Лунтик")
    ...             )
    ... )
    """
    pass