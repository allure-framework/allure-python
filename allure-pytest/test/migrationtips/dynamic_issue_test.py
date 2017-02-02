"""
>>> allure_report = getfixture('allure_report')
"""

import pytest


@pytest.fixture
def dynamic_issue(request):
    def mark(link):
        request.node.add_marker(pytest.allure.issue(link))
    return mark


@pytest.mark.parametrize('issue, result', [('ISSUE-1', True), ('ISSUE-2', False)])
def test_dynamic_issue(dynamic_issue, issue, result):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             all_of(
    ...                    has_test_case('test_dynamic_issue[ISSUE-1-True]',
    ...                                  has_link('ISSUE-1')),
    ...                    has_test_case('test_dynamic_issue[ISSUE-2-False]',
    ...                                  has_link('ISSUE-2'))
    ...             )
    ...  )
    """
    dynamic_issue(issue)
    assert result
