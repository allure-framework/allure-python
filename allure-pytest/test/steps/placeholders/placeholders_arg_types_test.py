# -*- coding: utf-8 -*-
"""
>>> allure_report = getfixture('allure_report')
"""

import allure
from struct import pack

TEMPLATE = u'arg is {0}, kwarg is {kwarg_parameter}, default is {default_parameter}'


@allure.step(TEMPLATE)
def step_with_parameters(arg_param, default_parameter=777, kwarg_parameter=None):
    pass


def test_primitive_type_parameters():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_primitive_type_parameters',
    ...                           has_step(TEMPLATE.format(False, kwarg_parameter=555, default_parameter=777))
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
    ...                           has_step(TEMPLATE.format(represent(pack('q', 0x0123456789)),
    ...                                                    kwarg_parameter=represent(pack('q', 0x0123456789)),
    ...                                                    default_parameter=777)
    ...                           )
    ...             )
    ... )
    """
    binary = pack('q', 0x0123456789)
    step_with_parameters(binary, kwarg_parameter=binary)


def test_text_type_parameters():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_text_type_parameters',
    ...                           has_step(TEMPLATE.format(represent('первый'),
    ...                                                    kwarg_parameter=represent('второй'),
    ...                                                    default_parameter=777)
    ...                           )
    ...             )
    ... )
    """
    step_with_parameters(u'первый', kwarg_parameter='второй')