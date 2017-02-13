"""
>>> allure_report = getfixture('allure_report')

>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(2)),
...                 has_property('test_groups', has_length(0))
...             )) # doctest: +SKIP
"""


def test_metafunc_param(metafunc_param):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_metafunc_param[True]',
    ...                           has_parameter('metafunc_param', True)
    ...             )
    ... )
    """
    assert metafunc_param


def test_metafunc_param_with_ids(metafunc_param_with_ids):
    """
    >>> allure_report = getfixture('allure_report') # doctest: +SKIP

    >>> assert_that(allure_report,
    ...             has_test_case('test_metafunc_param_with_ids[metafunc_param_id]',
    ...                           has_parameter('metafunc_param_id', True)
    ...             )
    ... ) # doctest: +SKIP

    >>> assert_that(allure_report,
    ...             has_test_case('test_metafunc_param_with_ids[metafunc_param_id]',
    ...                           has_parameter('metafunc_param_with_ids', True)
    ...             )
    ... ) # doctest: +SKIP
    """
    assert metafunc_param_with_ids
