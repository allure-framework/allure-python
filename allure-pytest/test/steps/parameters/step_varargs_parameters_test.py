# -*- coding: utf-8 -*-
"""
>>> allure_report = getfixture('allure_report')
"""

import allure


@allure.step("First step")
def step_with_varargs_parameters(arg_param, *varargs_parameter):
    pass


def test_without_varargs_parameters():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_without_varargs_parameters',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(False)),
    ...                                    has_parameter('varargs_parameter', represent(())),
    ...                            )
    ...             )
    ... )
    """
    step_with_varargs_parameters(False)


def test_single_vararg_parameter():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_vararg_parameter',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(False)),
    ...                                    has_parameter('varargs_parameter', represent((10,))),
    ...                                   )
    ...                           )
    ...            )
    """
    step_with_varargs_parameters(False, 10)


def test_many_varargs_parameters():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_many_varargs_parameters',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(False)),
    ...                                    has_parameter('varargs_parameter', represent(('abc', 30, True))),
    ...                           )
    ...             )
    ... )
    """
    step_with_varargs_parameters(False, 'abc', 30, True)
