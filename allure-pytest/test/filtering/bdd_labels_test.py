"""
>>> allure_report = getfixture('allure_report_with_params')('--allure-features=right_feature',
...                                                         '--allure-stories=right_story')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(4)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import pytest

def test_wihtout_features_and_stories():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_wihtout_features_and_stories',
    ...                           with_status('skipped')
    ...             )
    ... )
    """
    pass

@pytest.allure.feature('right_feature')
def test_right_feature_without_story():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_right_feature_without_story',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass

@pytest.allure.feature('wrong_feature')
@pytest.allure.story('right_story')
def test_wrong_feature_and_right_story():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_wrong_feature_and_right_story',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass

@pytest.allure.feature('right_feature')
@pytest.allure.story('wrong_story')
def test_right_feature_and_wrong_story():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_right_feature_and_wrong_story',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass
