# -*- coding: utf-8 -*-

import allure


@allure.description("""
This is a test description
with new lines..
""")
def test_dynamic_description():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_dynamic_description',
    ...                           has_description(
    ...                                           starts_with('It is a finally description')
    ...                           )
    ...             )
    ... )
    """
    allure.dynamic.description("It is a finally description")


@allure.description_html("""
<h1>This is a test description</h1>
<i>with new lines...</i>
""")
def test_dynamic_description_html():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_dynamic_description_html',
    ...                           has_description_html(
    ...                                           starts_with('<p>It is a finally description html</p>')
    ...                           )
    ...             )
    ... )
    """
    allure.dynamic.description_html("<p>It is a finally description html</p>")
