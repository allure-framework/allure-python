import pytest


@pytest.fixture
def fixture_one():
    yield


def test_func(fixture_one):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_func',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass