"""
>>> getfixture('inject_matchers')
>>> allure_report = getfixture('allure_report')
"""

from . import init_step

init_step()

def test_dummy():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_dummy')
    ... )
    """
    assert True