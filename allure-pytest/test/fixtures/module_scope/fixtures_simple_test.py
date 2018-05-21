import pytest


@pytest.fixture(scope='module')
def module_scope_simple_fixture():
    pass


def test_module_scope_simple_fixture(module_scope_simple_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_module_scope_simple_fixture',
    ...                           has_container(allure_report,
    ...                                         has_before('module_scope_simple_fixture')
    ...                           )
    ...             )
    ... )
    """
    pass


def test_reuse_module_scope_simple_fixture(module_scope_simple_fixture):
    """
    >>> allure_report = getfixture('allure_report')

    >>> assert_that(allure_report,
    ...             has_test_case('test_reuse_module_scope_simple_fixture',
    ...                           has_container(allure_report,
    ...                                         has_before('module_scope_simple_fixture')
    ...                           )
    ...             )
    ... )

    >>> assert_that(allure_report,
    ...             has_same_container('test_module_scope_simple_fixture',
    ...                                'test_reuse_module_scope_simple_fixture',
    ...                                has_before('module_scope_simple_fixture')
    ...                               )
    ... )
    """
    pass
