"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(5)),
...                 has_property('test_groups', has_length(4))
...             ))  # doctest: +SKIP

>>> assert_that(allure_report,
...             is_not(has_same_container('test_class_scope_fixture_in_function',
...                                       'test_again_class_scope_fixture_in_function',
...                                        has_before('class_scope_simple_fixture')
...                                      )
...             )
... )

>>> assert_that(allure_report,
...             is_not(has_same_container('test_class_scope_fixture_in_function',
...                                       'test_class_one_method_with_class_scope_fixture_one',
...                                        has_before('class_scope_simple_fixture')
...                                      )
...             )
... )

>>> assert_that(allure_report,
...             is_not(has_same_container('test_again_class_scope_fixture_in_function',
...                                       'test_class_two_method_with_class_scope_fixture_one',
...                                        has_before('class_scope_simple_fixture')
...                                      )
...             )
... )

"""

import pytest


@pytest.fixture(scope='class')
def class_scope_simple_fixture():
    pass


def test_class_scope_fixture_in_function(class_scope_simple_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_class_scope_fixture_in_function',
    ...                           has_container(allure_report,
    ...                                         has_before('class_scope_simple_fixture')
    ...                           )
    ...             )
    ... )
    """
    pass


def test_again_class_scope_fixture_in_function(class_scope_simple_fixture):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_again_class_scope_fixture_in_function',
    ...                           has_container(allure_report,
    ...                                         has_before('class_scope_simple_fixture')
    ...                           )
    ...             )
    ... )
    """
    pass


class TestClassOne(object):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_same_container('test_class_one_method_with_class_scope_fixture_one',
    ...                                'test_class_one_method_with_class_scope_fixture_two',
    ...                                has_before('class_scope_simple_fixture')
    ...             )
    ... )
    """

    def test_class_one_method_with_class_scope_fixture_one(self, class_scope_simple_fixture):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_class_one_method_with_class_scope_fixture_one',
        ...                           has_container(allure_report,
        ...                                         has_before('class_scope_simple_fixture')
        ...                           )
        ...             )
        ... )
        """
        pass

    def test_class_one_method_with_class_scope_fixture_two(self, class_scope_simple_fixture):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_class_one_method_with_class_scope_fixture_two',
        ...                           has_container(allure_report,
        ...                                         has_before('class_scope_simple_fixture')
        ...                           )
        ...             )
        ... )
        """
        pass


class TestClassTwo(object):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             is_not(has_same_container('test_class_one_method_with_class_scope_fixture_one',
    ...                                       'test_class_two_method_with_class_scope_fixture_one',
    ...                                       has_before('class_scope_simple_fixture')
    ...                                      )
    ...             )
    ... )
    """
    def test_class_two_method_with_class_scope_fixture_one(self, class_scope_simple_fixture):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_class_two_method_with_class_scope_fixture_one',
        ...                           has_container(allure_report,
        ...                                         has_before('class_scope_simple_fixture')
        ...                           )
        ...             )
        ... )
        """
        pass
