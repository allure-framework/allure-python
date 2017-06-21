"""
>>> allure_report = getfixture('allure_report')

COUNT OF CASES AND GROUPS
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(10)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""
import pytest


@pytest.mark.parametrize('param', [True, False])
def test_parametrization_one_param_without_ids(param):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param in [True, False]:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_parametrization_one_param_without_ids[{param}]'.format(param=param),
    ...                               has_parameter('param', str(param))
    ...                ))
    """
    assert not param


@pytest.mark.parametrize('param', [True, False], ids=['pass', 'fail'])
def test_parametrization_one_param_with_ids(param):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param in [True, False]:
    ...     ids = 'pass' if param else 'fail'
    ...     assert_that(allure_report,
    ...                 has_test_case('test_parametrization_one_param_with_ids[{param}]'.format(param=ids),
    ...                               has_parameter(ids, str(param))
    ...                ))
    """
    assert not param


@pytest.mark.parametrize('param1, param2', [(True, False), (True, True)])
def test_parametrization_many_params_as_string_without_ids(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param1, param2 in [(True, False), (True, True)]:
    ...     test_case = 'test_parametrization_many_params_as_string_without_ids'
    ...     assert_that(allure_report,
    ...                 has_test_case('{test_case}[{param1}-{param2}]'.format(test_case=test_case, param1=param1, param2=param2),
    ...                               all_of(has_parameter('param1', str(param1)),
    ...                                      has_parameter('param2', str(param2))
    ...                              )
    ...                 ))
    """
    assert param1 and param2


@pytest.mark.parametrize(['param1', 'param2'], [(True, False), (True, True)])
def test_parametrization_many_params_as_iterable_without_ids(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param1, param2 in [(True, False), (True, True)]:
    ...     test_case = 'test_parametrization_many_params_as_iterable_without_ids'
    ...     assert_that(allure_report,
    ...                 has_test_case('{test_case}[{param1}-{param2}]'.format(test_case=test_case, param1=param1, param2=param2),
    ...                               all_of(has_parameter('param1', str(param1)),
    ...                                      has_parameter('param2', str(param2))
    ...                              )
    ...                 ))
    """
    assert param1 and param2


@pytest.mark.parametrize('param1, param2', [(True, False), (True, True)], ids=['fail', 'pass'])
def test_parametrization_many_params_with_ids(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param1, param2 in [(True, False), (True, True)]:
    ...     ids = 'pass' if param1 and param2 else 'fail'
    ...     assert_that(allure_report,
    ...                 has_test_case('test_parametrization_many_params_with_ids[{ids}]'.format(ids=ids),
    ...                               all_of(
    ...                                   has_parameter('{ids}::{param}'.format(ids=ids, param='param1'), str(param1)),
    ...                                   has_parameter('{ids}::{param}'.format(ids=ids, param='param2'), str(param2))
    ...                               )
    ...                 ))

    """
    assert param1 and param2


