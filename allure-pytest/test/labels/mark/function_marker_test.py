# -*- coding: utf-8 -*-
"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(3)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest


@pytest.mark.cool
@pytest.mark.stuff
def test_pytest_marker():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...                 has_test_case('test_pytest_marker',
    ...                     has_tag('@pytest.mark.cool'),
    ...                     has_tag('@pytest.mark.stuff')
    ...                 )
    ...             )
    """
    pass


@pytest.mark.marker('cool', 'stuff')
def test_pytest_marker_with_args():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...                 has_test_case('test_pytest_marker_with_args',
    ...                     has_tag("@pytest.mark.marker('cool', 'stuff')")
    ...                 )
    ...             )
    """
    pass


@pytest.mark.marker(stuff='cool')
def test_pytest_marker_with_kwargs():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_marker_with_kwargs',
    ...                           has_tag("@pytest.mark.marker(stuff='cool')")
    ...                           )
    ...             )
    """
    pass


@pytest.mark.marker(stuff='я')
def test_pytest_marker_with_kwargs_native_encoding():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_marker_with_kwargs_native_encoding',
    ...                           has_tag("@pytest.mark.marker(stuff=%s)" % represent('я'))
    ...                          )
    ...             )
    """
    pass


@pytest.mark.marker(stuff=u'я')
def test_pytest_marker_with_kwargs_utf_encoding():
    """
    >>> from allure_commons.utils import represent
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_marker_with_kwargs_utf_encoding',
    ...                           has_tag("@pytest.mark.marker(stuff=%s)" % represent('я'))
    ...                          )
    ...             )
    """
    pass


@pytest.mark.marker('that', stuff='cool')
def test_pytest_marker_with_args_and_kwargs():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_pytest_marker_with_args_and_kwargs',
    ...                           has_tag("@pytest.mark.marker('that', stuff='cool')")
    ...                          )
    ...             )
    """
    pass
