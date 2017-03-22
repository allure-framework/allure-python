"""
>>> allure_report = getfixture('allure_report')

>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(6)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest


def test_history_id():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_history_id',
    ...                           has_history_id()
    ...             )
    ... )
    """
    pytest.exit("Just test")