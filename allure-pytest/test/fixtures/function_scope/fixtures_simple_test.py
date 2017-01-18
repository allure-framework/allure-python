"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(5)),
...                 has_property('test_groups', has_length(0))
...             ))
"""

import pytest


@pytest.fixture
def function_scope_simple_fixture():
    pass


def test_function_scope_simple_fixture(function_scope_simple_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    ...     assert_that(allure_report,
    ...                 has_test_case('test_function_scope_simple_fixture',
    ...                     has_before('function_scope_simple_fixture')
    ...                 ))
    """
    pass


def test_reuse_function_scope_simple_fixture(function_scope_simple_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    ...     assert_that(allure_report,
    ...                 has_test_case('test_reuse_function_scope_simple_fixture',
    ...                     has_before('function_scope_simple_fixture')
    ...                 ))
    """
    pass


@pytest.fixture
def one_more_function_scope_fixture():
    pass


def test_with_two_function_scope_fixtures(function_scope_simple_fixture, one_more_function_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_with_two_function_scope_fixtures',
    ...                 all_of(
    ...                     has_before('function_scope_simple_fixture'),
    ...                     has_before('one_more_function_scope_fixture')
    ...                 )
    ...             )
    ... )
    """
    pass


@pytest.fixture
def nested_function_scope_fixture(function_scope_simple_fixture):
    pass


def test_nested_function_scope_fixtures(nested_function_scope_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_nested_function_scope_fixtures',
    ...                 all_of(
    ...                     has_before('function_scope_simple_fixture'),
    ...                     has_before('nested_function_scope_fixture')
    ...                 )
    ...             )
    ... )
    """
    pass


@pytest.fixture
def function_scope_fixture_wich_depends_on_two_other(function_scope_simple_fixture, one_more_function_scope_fixture):
    pass


def test_with_apple_pineapple_pen_fixture(function_scope_fixture_wich_depends_on_two_other):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_with_apple_pineapple_pen_fixture',
    ...                 all_of(
    ...                     has_before('function_scope_simple_fixture'),
    ...                     has_before('one_more_function_scope_fixture'),
    ...                     has_before('function_scope_fixture_wich_depends_on_two_other')
    ...                 )
    ...             ))
    """
    pass
