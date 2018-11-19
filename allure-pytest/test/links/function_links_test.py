"""
>>> allure_report = getfixture('allure_report')

>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(6)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import allure

LINK = 'http://qameta.io'
LINK_NAME = 'QAMETA'
LINK_TYPE = 'homepage'
ISSUE = 'https://github.com/qameta/allure-integrations/issues/8'
ISSUE_NAME = 'Github issue'
TEST_CASE = 'https://github.com/qameta/allure-integrations/issues/8#issuecomment-268313637'
ANOTHER_TEST_CASE = 'https://github.com/allure-framework/allure-python/issues/191'
TEST_CASE_NAME = 'Comment with spec'


@allure.link(LINK)
def test_single_link():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_link',
    ...                 has_link(LINK)
    ...             ))

    """
    pass


@allure.link(LINK, name=LINK_NAME)
def test_single_named_link():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_named_link',
    ...                 has_link(LINK, name=LINK_NAME)
    ...             ))

    """
    pass


@allure.link(LINK, name=LINK_NAME, link_type=LINK_TYPE)
def test_single_named_link_with_custom_type():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_named_link_with_custom_type',
    ...                 has_link(LINK, name=LINK_NAME, link_type=LINK_TYPE)
    ...             ))
    """
    pass


@allure.issue(ISSUE)
def test_single_issue():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_issue',
    ...                 has_issue_link(ISSUE)
    ...             ))
    """
    pass


@allure.testcase(TEST_CASE)
def test_single_test_case():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_single_test_case',
    ...                 has_test_case_link(TEST_CASE)
    ...             ))
    """
    pass


@allure.link(LINK, name=LINK_NAME, link_type=LINK_TYPE)
@allure.testcase(TEST_CASE, name=TEST_CASE_NAME)
@allure.issue(ISSUE, name=ISSUE_NAME)
def test_with_links_cases_and_issues():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_with_links_cases_and_issues',
    ...                 has_link(LINK, name=LINK_NAME, link_type=LINK_TYPE),
    ...                 has_test_case_link(TEST_CASE, name=TEST_CASE_NAME),
    ...                 has_issue_link(ISSUE, name=ISSUE_NAME)
    ...             ))
    """
    pass


@allure.testcase(TEST_CASE, name="First")
@allure.testcase(ANOTHER_TEST_CASE, name="Second")
def test_multiply_some_type_links():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_multiply_some_type_links',
    ...                 has_test_case_link(TEST_CASE, name='First'),
    ...                 has_test_case_link(ANOTHER_TEST_CASE, name='Second')
    ...             ))
    """