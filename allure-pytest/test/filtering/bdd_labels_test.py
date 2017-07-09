"""
>>> allure_report = getfixture('allure_report_with_params')('--allure-epic=right_epic',
...                                                         '--allure-features=right_feature',
...                                                         '--allure-stories=right_story')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(4)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import allure


def test_without_epic_features_and_stories():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-epic=right_epic',
    ...                                                         '--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_without_epic_features_and_stories',
    ...                           with_status('skipped')
    ...             )
    ... )
    """
    pass


@allure.feature('right_feature')
def test_right_feature_without_story_and_epic():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-epic=right_epic',
    ...                                                         '--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_right_feature_without_story_and_epic',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass


@allure.feature('wrong_epic')
@allure.feature('wrong_feature')
@allure.story('right_story')
def test_right_story_but_wrong_epic_and_feature():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-epic=right_epic',
    ...                                                         '--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_right_story_but_wrong_epic_and_feature',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass


@allure.feature('wrong_epic')
@allure.feature('right_feature')
@allure.story('wrong_story')
def test_right_feature_but_wrong_epic_and_story():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-epic=right_epic',
    ...                                                         '--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_right_feature_but_wrong_epic_and_story',
    ...                           with_status('passed')
    ...             )
    ... )
    """
    pass


@allure.feature('wrong_epic')
@allure.feature('wrong_feature')
@allure.story('wrong_story')
def test_wrong_epic_feature_and_story():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-epic=right_epic',
    ...                                                         '--allure-features=right_feature',
    ...                                                         '--allure-stories=right_story')
    >>> assert_that(allure_report,
    ...             has_test_case('test_wrong_epic_feature_and_story',
    ...                           with_status('skipped')
    ...             )
    ... )
    """
    pass
