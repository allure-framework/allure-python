"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(3)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import allure


@allure.label('has_label', 'work', 'cool')
def test_user_label():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_user_label',
    ...                 all_of(
    ...                     has_label('has_label', 'work'),
    ...                     has_label('has_label', 'cool'),
    ...                 )
    ...             ))
    """
    pass

'''
def test_user_dynamic_label():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_user_label',
    ...                 all_of(
    ...                     has_label('has_label', 'work'),
    ...                     has_label('has_label', 'cool'),
    ...                 )
    ...             ))
    """
    allure.dynamc.label('has_label', 'work', 'cool')
    pass
'''