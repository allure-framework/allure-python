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
    ...                     has_tag('cool'),
    ...                     has_tag('stuff')
    ...                 )
    ...             )
    """
    pass


@pytest.mark.usermark1
@pytest.mark.usermark2
@pytest.mark.parametrize("param", ["foo"])
@pytest.mark.skipif(False, reason="reason2")
@pytest.mark.skipif(False, reason="reason1")
def test_omit_pytest_markers(param):
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...                 has_test_case('test_omit_pytest_markers[foo]',
    ...                     has_tag("usermark1"),
    ...                     has_tag("usermark2"),
    ...                     is_not(has_tag("skipif(False, reason='reason2')")),
    ...                     is_not(has_tag("skipif(False, reason='reason1')")),
    ...                     is_not(has_tag("parametrize('param', ['foo'])")),
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
    ...                     has_tag("marker('cool', 'stuff')")
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
    ...                           has_tag("marker(stuff='cool')")
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
    ...                           has_tag("marker(stuff=%s)" % represent('я'))
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
    ...                           has_tag("marker(stuff=%s)" % represent('я'))
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
    ...                           has_tag("marker('that', stuff='cool')")
    ...                          )
    ...             )
    """
    pass
