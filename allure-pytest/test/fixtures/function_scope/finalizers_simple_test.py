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
def fixture_with_passed_finalizer(request):
    def passed_finalizer():
        pass
    request.addfinalizer(passed_finalizer)


@pytest.fixture
def fixture_failed_finalizer(request):
    def failed_finalizer():
        assert False
    request.addfinalizer(failed_finalizer)


@pytest.fixture
def fixture_with_two_finalizers(request):
    def first_finalizer():
        pass
    request.addfinalizer(first_finalizer)

    def second_finalizer():
        pass
    request.addfinalizer(second_finalizer)


def test_two_fixures_with_finalizer(fixture_with_passed_finalizer, fixture_failed_finalizer):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_two_fixures_with_finalizer',
    ...                           has_container(allure_report,
    ...                                         has_before('fixture_with_passed_finalizer'),
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='fixture_with_passed_finalizer',
    ...                                                               finalizer='passed_finalizer'),
    ...                                                   with_status('passed')
    ...                                         )
    ...                           ),
    ...                           has_container(allure_report,
    ...                                         has_before('fixture_failed_finalizer'),
    ...                                         has_after('{fixture}::{finalizer}'.format(
    ...                                                               fixture='fixture_failed_finalizer',
    ...                                                               finalizer='failed_finalizer'),
    ...                                                   with_status('failed'),
    ...                                                   has_status_details(
    ...                                                                       with_status_message('AssertionError')
    ...                                                   )
    ...                                         )
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
