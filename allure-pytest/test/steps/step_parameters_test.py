"""
>>> allure_report = getfixture('allure_report')
"""

import pytest


@pytest.allure.step("First step")
def step_with_parameters(step_fail, default_value=777, named_parameter=888):
    assert not step_fail


def test_outside_step_with_parameters():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_step_with_parameters',
    ...                           has_step('First step',
    ...                                    has_parameter('step_fail', False),
    ...                                    has_parameter('default_value', 777),
    ...                                    has_parameter('named_parameter', 555),
    ...                            )
    ...             )
    ... )
    """
    step_with_parameters(False, named_parameter=555)
