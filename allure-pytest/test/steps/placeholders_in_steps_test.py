"""
>>> allure_report = getfixture('allure_report')

>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(6)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest


@pytest.allure.step('arg is {0}')
def step_with_equal_args(step_arg_param):
    assert step_arg_param


def test_equal_args_and_places():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_equal_args_and_places',
    ...                           has_step('arg is {0}'.format(True),
    ...                                    has_parameter('step_arg_param', True)
    ...                           )
    ...             )
    ... )
    """
    step_with_equal_args(True)


@pytest.allure.step('arg is {0}')
def step_places_less(step_arg_param1, step_arg_param2):
    assert step_arg_param1 and step_arg_param2


def test_places_less():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_places_less',
    ...                           has_step('arg is {0}'.format(True, True),
    ...                                    has_parameter('step_arg_param1', True),
    ...                                    has_parameter('step_arg_param2', True)
    ...                           )
    ...             )
    ... )
    """
    step_places_less(True, True)


@pytest.allure.step('arg are {0} and {1}')
def step_args_less(step_arg_param,):
    assert step_arg_param


def test_args_less():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_args_less',
    ...                           has_status_details(
    ...                                              with_status_message('IndexError: tuple index out of range')
    ...                           )
    ...             )
    ... )
    """
    step_args_less(True)
