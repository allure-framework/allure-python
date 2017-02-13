"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(2)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest


@pytest.fixture
def fixture_with_finalizer_a(request):
    def finalizer_fixture_a():
        pass
    request.addfinalizer(finalizer_fixture_a)


@pytest.fixture
def fixture_with_finalizer_b(request):
    def finalizer_fixture_b():
        pass
    request.addfinalizer(finalizer_fixture_b)


@pytest.fixture
def fixture_with_two_finalizers(request):
    def first_finalizer():
        pass
    request.addfinalizer(first_finalizer)

    def second_finalizer():
        pass
    request.addfinalizer(second_finalizer)


def test_two_fixures_with_finalizer(fixture_with_finalizer_a, fixture_with_finalizer_b):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_two_fixures_with_finalizer',
    ...                           has_container(allure_report,
    ...                                         has_before('fixture_with_finalizer_a'),
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='fixture_with_finalizer_a',
    ...                                                               finalizer='finalizer_fixture_a'))
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                         has_before('fixture_with_finalizer_b'),
    ...                                                               fixture='fixture_with_finalizer_b',
    ...                                                               finalizer='finalizer_fixture_b'))
    ...                           )
    ...             )
    ... )
    """
    pass


def test_fixture_with_two_finalizer(fixture_with_two_finalizers):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_fixture_with_two_finalizer',
    ...                           has_container(allure_report,
    ...                                         has_before('fixture_with_two_finalizers'),
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='fixture_with_two_finalizers',
    ...                                                               finalizer='first_finalizer')),
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='fixture_with_two_finalizers',
    ...                                                               finalizer='second_finalizer'))
    ...                           )
    ...              )
    ... )
    """
    pass
