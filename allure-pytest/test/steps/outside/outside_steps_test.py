"""
>>> getfixture('inject_matchers')
>>> allure_report = getfixture('allure_report')
"""

from . import init_step


def test_step_from_init_py():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_step_from_init_py',
    ...                           has_step('step in __init__.py')
    ...             )
    ... )
    """
    init_step()


def test_step_from_conftest(fixture_with_conftest_step):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_step_from_conftest',
    ...                           has_container(allure_report,
    ...                                         has_before('fixture_with_conftest_step',
    ...                                                    has_step('step in conftest.py')
    ...                                         )
    ...                           )
    ...             )
    ... )
    """
    pass
