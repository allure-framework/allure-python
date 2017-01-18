"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(28)),
...                 has_property('test_groups', has_length(0))
...             ))
"""

import pytest


@pytest.mark.parametrize('param1', [True, False])
@pytest.mark.parametrize('param2', [True, True])
def test_parametrization_many_decorators_without_ids(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for num1, (param1, ids1) in enumerate(zip((True, False), ('param1_id1', 'param1_id2'))):
    ...     for num2, (param2, ids2) in enumerate(zip((True, True), ('param2_id1', 'param2_id2'))):
    ...         test_case = 'test_parametrization_many_decorators_without_ids'
    ...         assert_that(allure_report,
    ...                     has_test_case('{test_case}[{param2}{num2}-{param1}]'.format(test_case=test_case,
    ...                                                                                param1=param1,
    ...                                                                                param2=param2,
    ...                                                                                num2=num2),
    ...                                   all_of(
    ...                                       has_parameter('param1', param1),
    ...                                       has_parameter('param2', param2)
    ...                                    )
    ...                     ))
    """
    assert param1 and param2


@pytest.mark.parametrize('param1', [True, False], ids=['param1_id1', 'param1_id2'])
@pytest.mark.parametrize('param2', [True, True])
def test_parametrization_with_many_decorators_and_ids_for_first(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for num1, (param1, ids1) in enumerate(zip((True, False), ('param1_id1', 'param1_id2'))):
    ...     for num2, (param2, ids2) in enumerate(zip((True, True), ('param2_id1', 'param2_id2'))):
    ...         test_case = 'test_parametrization_with_many_decorators_and_ids_for_first'
    ...         assert_that(allure_report,
    ...                     has_test_case('{test_case}[{param2}{num2}-{ids1}]'.format(test_case=test_case,
    ...                                                                                ids1=ids1,
    ...                                                                                param2=param2,
    ...                                                                                num2=num2),
    ...                                   all_of(
    ...                                       has_parameter(ids1, param1),
    ...                                       has_parameter('param2', param2)
    ...                                   )
    ...                     ))
    """
    assert param1 and param2


@pytest.mark.parametrize('param1', [True, False])
@pytest.mark.parametrize('param2', [True, True], ids=['param2_id1', 'param2_id2'])
def test_parametrization_with_many_decorators_and_ids_for_second(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for num1, (param1, ids1) in enumerate(zip((True, False), ('param1_id1', 'param1_id2'))):
    ...     for num2, (param2, ids2) in enumerate(zip((True, True), ('param2_id1', 'param2_id2'))):
    ...         test_case = 'test_parametrization_with_many_decorators_and_ids_for_second'
    ...         assert_that(allure_report,
    ...                     has_test_case('{test_case}[{ids2}-{param1}]'.format(test_case=test_case,
    ...                                                                         param1=param1,
    ...                                                                         ids2=ids2),
    ...                                   all_of(
    ...                                       has_parameter('param1', param1),
    ...                                       has_parameter(ids2, param2)
    ...                                   )
    ...                     ))
    """
    assert param1 and param2


@pytest.mark.parametrize('param1', [True, False], ids=['param1_id1', 'param1_id2'])
@pytest.mark.parametrize('param2', [True, True], ids=['param2_id1', 'param2_id2'])
def test_parametrization_with_many_decorators_and_ids_for_all(param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for num1, (param1, ids1) in enumerate(zip((True, False), ('param1_id1', 'param1_id2'))):
    ...     for num2, (param2, ids2) in enumerate(zip((True, True), ('param2_id1', 'param2_id2'))):
    ...         test_case = 'test_parametrization_with_many_decorators_and_ids_for_all'
    ...         assert_that(allure_report,
    ...                     has_test_case('{test_case}[{ids2}-{ids1}]'.format(test_case=test_case,
    ...                                                                         ids1=ids1,
    ...                                                                         ids2=ids2),
    ...                                   all_of(
    ...                                       has_parameter(ids1, param1),
    ...                                       has_parameter(ids2, param2)
    ...                                   )
    ...                     ))
    """
    assert param1 and param2


@pytest.mark.parametrize('param1', [True, False],)
@pytest.mark.parametrize('param2', [True, False], ids=['param2_id1', 'param2_id2'])
@pytest.mark.parametrize('param3', [True, True, False], ids=['param3_id1', 'param3_id2', 'param3_id3'])
def test_parametrization_with_many_decorators_with_partial_ids_and_unsorted_args(param3, param1, param2):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for param1 in [True, False]:
    ...     for param2, ids2 in zip((True, False), ('param2_id1', 'param2_id2')):
    ...         for param3, ids3 in zip((True, True), ('param3_id1', 'param3_id2', 'param3_id3')):
    ...
    ...             test_case = 'test_parametrization_with_many_decorators_with_partial_ids_and_unsorted_args'
    ...             assert_that(allure_report,
    ...                         has_test_case('{test_case}[{ids3}-{ids2}-{param1}]'.format(test_case=test_case,
    ...                                                                                    param1=param1,
    ...                                                                                    ids2=ids2,
    ...                                                                                    ids3=ids3),
    ...                                   all_of(
    ...                                       has_parameter('param1', param1),
    ...                                       has_parameter(ids2, param2),
    ...                                       has_parameter(ids3, param3)
    ...                                    )
    ...                     ))
    """
    assert param1 and param2 or param3
