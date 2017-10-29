# -*- coding: utf-8 -*-

import pytest


@pytest.mark.parametrize('param', [True], ids=['Болек'])
def test_parametrization_native_ids_encoding(param):
    """
    >>> import six
    >>> allure_report = getfixture('allure_report')
    >>> param = 'Болек'
    >>> test_case = 'test_parametrization_native_ids_encoding[{param}]'.format(param=param)
    >>> if six.PY2:
    ...     test_case = test_case.decode('utf-8')
    >>> assert_that(allure_report, has_test_case(test_case))
    """
    pass


@pytest.mark.parametrize('param', [True], ids=[u'Лёлек'])
def test_parametrization_utf_ids_encoding(param):
    """
    >>> import six
    >>> allure_report = getfixture('allure_report')
    >>> if six.PY2:
    ...     param = 'Лёлек'.decode('utf-8')
    ...     test_case = u'test_parametrization_utf_ids_encoding[{param}]'.format(param=param)
    ...     assert_that(allure_report, has_test_case(test_case))
    ... else:
    ...     param = 'Лёлек'
    ...     test_case = 'test_parametrization_utf_ids_encoding[{param}]'.format(param=param)
    ...     assert_that(allure_report, has_test_case(test_case))
    """
    pass
