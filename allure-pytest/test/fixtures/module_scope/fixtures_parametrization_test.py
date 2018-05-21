import pytest
import allure


PARAMS = ["first", "second", "third"]


@pytest.fixture(scope='module', params=PARAMS)
def module_scope_parametrized_fixture():
    pass


def test_module_scope_parametrized_fixture(module_scope_parametrized_fixture):
    """
    >>> allure_report = getfixture('allure_report')

    >>> for param in PARAMS:
    ...    assert_that(allure_report,
    ...                has_test_case('test_module_scope_parametrized_fixture[{param}]'.format(param=param),
    ...                              has_container(allure_report,
    ...                                           has_before('module_scope_parametrized_fixture')
    ...                              )
    ...                )
    ... )
    """
    pass


def test_reuse_module_scope_parametrized_fixture(module_scope_parametrized_fixture):
    """
    >>> allure_report = getfixture('allure_report')

    >>> for param in PARAMS:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_reuse_module_scope_parametrized_fixture[{param}]'.format(param=param),
    ...                               has_container(allure_report,
    ...                                            has_before('module_scope_parametrized_fixture')
    ...                               )
    ...                 )
    ...     )

    >>> for param in PARAMS:
    ...     assert_that(allure_report,
    ...                 has_same_container('test_module_scope_parametrized_fixture[{param}]'.format(param=param),
    ...                                    'test_reuse_module_scope_parametrized_fixture[{param}]'.format(param=param),
    ...                                    has_before('module_scope_parametrized_fixture')
    ...                                   )
    ...     )
    """
    pass
