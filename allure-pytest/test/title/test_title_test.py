# -*- coding: utf-8 -*-
import allure


@allure.title("A some test tile")
def test_title():
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
