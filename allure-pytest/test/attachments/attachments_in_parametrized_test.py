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

BODY = ['I Like to', 'Move It']


@pytest.mark.parametrize('attachment', BODY)
def test_attach_data_from_parametrized_test(attachment):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for body in BODY:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_attach_data_from_parametrized_test[{body}]'.format(body=body),
    ...                              has_attachment()
    ...                )
    ...     )
    """
    allure.attach(attachment)
