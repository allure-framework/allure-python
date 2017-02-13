"""
>>> allure_report = getfixture('allure_report')
"""

import pytest


@pytest.fixture(scope='session', params=[True, False], ids=['session_true', 'session_false'])
def session_scope_param(request):
    return request.param


@pytest.fixture(scope='class', params=[True, False], ids=['class_true', 'class_false'])
def class_scope_param(request):
    return request.param


@pytest.fixture(params=[True, False], ids=['function_true', 'function_false'])
def function_scope_param(request):
    return request.param


class TestClassParams(object):

    def test_method_with_direct_params_order(self, session_scope_param, class_scope_param, function_scope_param):
        """
        >>> allure_report = getfixture('allure_report')
        >>> for session_scope_value, session_scope_id in zip([True, False], ['session_true', 'session_false']):
        ...     for class_scope_value, class_scope_id in zip([True, False], ['class_true', 'class_false']):
        ...         for function_scope_value, function_scope_id in zip([True, False], ['function_true', 'function_false']):
        ...             assert_that(allure_report,
        ...                         has_test_case('test_method_with_direct_params_order[{session_param}-{class_param}-{function_param}]'.format(
        ...                                       session_param=session_scope_id,
        ...                                       class_param=class_scope_id,
        ...                                       function_param=function_scope_id),
        ...                                       all_of(has_parameter(session_scope_id, session_scope_value),
        ...                                              has_parameter(class_scope_id, class_scope_value),
        ...                                              has_parameter(function_scope_id, function_scope_value)
        ...                                       )
        ...                         )
        ...             ) # doctest: +SKIP

        """
        assert session_scope_param or class_scope_param or function_scope_param
