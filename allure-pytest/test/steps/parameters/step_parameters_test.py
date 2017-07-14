# -*- coding: utf-8 -*-
"""
>>> allure_report = getfixture('allure_report')
"""

import allure
from struct import pack


@allure.step("First step")
def step_with_parameters(arg_param, default_parameter=777, kwarg_parameter=None):
    pass


def test_primitive_type_parameters():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_primitive_type_parameters',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(False)),
    ...                                    has_parameter('default_parameter', represent(777)),
    ...                                    has_parameter('kwarg_parameter', represent(555)),
    ...                            )
    ...             )
    ... )
    """
    step_with_parameters(False, kwarg_parameter=555)


def test_binary_type_parameters():
    """
    >>> from struct import pack
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_binary_type_parameters',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent(pack('q', 0x0123456789))),
    ...                                    has_parameter('kwarg_parameter', represent(pack('q', 0x0123456789))),
    ...                                   )
    ...                           )
    ...            )
    """
    binary = pack('q', 0x0123456789)
    step_with_parameters(binary, kwarg_parameter=binary)


def test_text_type_parameters():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_text_type_parameters',
    ...                           has_step('First step',
    ...                                    has_parameter('arg_param', represent('первый')),
    ...                                    has_parameter('kwarg_parameter', represent('второй')),
    ...                           )
    ...             )
    ... )
    """
    step_with_parameters(u'первый', kwarg_parameter='второй')