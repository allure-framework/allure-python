# -*- coding: utf-8 -*-
"""
>>> allure_report = getfixture('allure_report')
"""


def test_text_description():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_text_description',
    ...                           has_description(
    ...                                           starts_with('\\n    >>> allure_report = ')
    ...                           )
    ...             )
    ... )
    """
    pass


def test_utf8_text_description():
    u"""
    >>> #  рекурсия
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_utf8_text_description',
    ...                           has_description(
    ...                                           starts_with(u'\\n    >>> #  рекурсия')
    ...                           )
    ...             )
    ... )
    """
    pass