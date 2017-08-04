"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(9)),
...                 has_property('test_groups', has_length(0)),
...                 has_property('attachments', has_length(11))
...             ))  # doctest: +SKIP
"""

import allure
import pytest


@pytest.mark.parametrize('attachment', ['body'])
def test_attach_data_from_parametrized_test(attachment):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_attach_data_from_parametrized_test',
    ...                           has_attachment()
    ...             )
    ... )
    """
    allure.attach(attachment)
