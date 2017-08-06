"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(8)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest


@pytest.fixture(params=[True, False])
def parametrized_fixture(request):
    return request.param


def test_function_scope_parametrized_fixture(parametrized_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param in [True, False]:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_function_scope_parametrized_fixture[{param}]'.format(param=param),
    ...                               has_parameter('parametrized_fixture', str(param))
    ...                 )
    ...     )
    """
    assert parametrized_fixture


@pytest.fixture(params=[True, False], ids=['param_true', 'param_false'])
def parametrized_fixture_with_ids(request):
    return request.param


def test_function_scope_parametrized_fixture_with_ids(parametrized_fixture_with_ids):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param, ids in zip([True, False], ['param_true', 'param_false']):
    ...     assert_that(allure_report,
    ...                 has_test_case('test_function_scope_parametrized_fixture_with_ids[{ids}]'.format(ids=ids),
    ...                               has_parameter('parametrized_fixture_with_ids', str(param))
    ...                 )
    ...     )
    """
    assert parametrized_fixture_with_ids


def test_two_function_scope_parametrized_fixture(parametrized_fixture, parametrized_fixture_with_ids):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param1 in [True, False]:
    ...     for param2, ids2 in zip([True, False], ['param_true', 'param_false']):
    ...         assert_that(allure_report,
    ...                     has_test_case('test_two_function_scope_parametrized_fixture[{param1}-{ids2}]'.format(
    ...                                                                                         param1=param1, ids2=ids2),
    ...                         all_of(has_parameter('parametrized_fixture', str(param1)),
    ...                                has_parameter('parametrized_fixture_with_ids', str(param2))
    ...                         )
    ...                     )
    ...         )
    """
    assert parametrized_fixture_with_ids and parametrized_fixture
