import os
import pytest


def test_register_unregister():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_register_unregister',
    ...                           with_status('passed')
    ...              )
    ... )
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    target = os.path.join(current_dir, 'sample.py')
    assert pytest.main(['--alluredir=/tmp', target]) == 0
    assert pytest.main(['--alluredir=/tmp', target]) == 0

