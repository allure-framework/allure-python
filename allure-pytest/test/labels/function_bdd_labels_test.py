"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(3)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest


@pytest.allure.feature('single feature')
def test_single_feature_label():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_feature_label',
    ...                 has_feature('single feature')
    ...             ))
    """
    pass


@pytest.allure.story('single story')
def test_single_story_label():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_story_label',
    ...                 has_story('single story')
    ...             ))
    """
    pass


@pytest.allure.feature('feature one', 'feature two')
@pytest.allure.story('story one', 'story two')
def test_many_bdd_labels_for_one_function():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_many_bdd_labels_for_one_function',
    ...                 all_of(
    ...                     has_feature('feature one'),
    ...                     has_feature('feature two'),
    ...                     has_story('story one'),
    ...                     has_story('story two')
    ...                 )
    ...             ))
    """
    pass
