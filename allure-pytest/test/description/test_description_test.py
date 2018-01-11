# -*- coding: utf-8 -*-

"""
>>> allure_report = getfixture('allure_report')
"""

import allure


@allure.description("""
This is a test description
with new lines..
""")
def test_description():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_description',
    ...                           has_description(
    ...                                           starts_with('\\nThis is a test description')
    ...                           )
    ...             )
    ... )
    """
    pass


@allure.description_html("""
<h1>This is a test description</h1>
<i>with new lines...</i>
""")
def test_description_html():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_description_html',
    ...                           has_description_html(
    ...                                           starts_with('\\n<h1>This is a test description</h1>')
    ...                           )
    ...             )
    ... )
    """
    pass


def test_docstring_description():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_docstring_description',
    ...                           has_description(
    ...                                           starts_with('\\n    >>> allure_report = ')
    ...                           )
    ...             )
    ... )
    """
    pass


def test_unicode_docstring_description():
    u"""
    >>> #  рекурсия
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_unicode_docstring_description',
    ...                           has_description(
    ...                                           starts_with(u'\\n    >>> #  рекурсия')
    ...                           )
    ...             )
    ... )
    """
    pass
