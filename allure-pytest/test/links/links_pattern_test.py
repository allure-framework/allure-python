import pytest
import allure


ISSUE = '24'
ISSUE_PATTERN = 'https://github.com/allure-framework/allure-python2/issues/{}'
CUSTOM_LINK_TYPE = 'docs'
CUSTOM_LINK_PATTERN = 'https://docs.qameta.io/allure/2.0/integration/{}/'
CUSTOM_LINK = 'pytest'


@allure.issue(ISSUE)
@allure.link(CUSTOM_LINK, link_type=CUSTOM_LINK_TYPE)
def test_link_pattern():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-link-pattern=issue:{pattern}'.format(
    ...                                                             pattern=ISSUE_PATTERN),
    ...                                                         '--allure-link-pattern={link_type}:{pattern}'.format(
    ...                                                             link_type=CUSTOM_LINK_TYPE,
    ...                                                             pattern=CUSTOM_LINK_PATTERN))
    >>> assert_that(allure_report,
    ...             has_test_case('test_link_pattern',
    ...                           has_link(ISSUE_PATTERN.format(ISSUE)),
    ...                           has_link(CUSTOM_LINK_PATTERN.format(CUSTOM_LINK))
    ...                           )
    ...             )
    """
    pass


def test_dynamic_link_pattern():
    """
    >>> allure_report = getfixture('allure_report_with_params')('--allure-link-pattern=issue:{pattern}'.format(
    ...                                                             pattern=ISSUE_PATTERN),
    ...                                                         '--allure-link-pattern={link_type}:{pattern}'.format(
    ...                                                             link_type=CUSTOM_LINK_TYPE,
    ...                                                             pattern=CUSTOM_LINK_PATTERN))
    >>> assert_that(allure_report,
    ...             has_test_case('test_dynamic_link_pattern',
    ...                           has_link(ISSUE_PATTERN.format(ISSUE)),
    ...                           has_link(CUSTOM_LINK_PATTERN.format(CUSTOM_LINK))
    ...                           )
    ...             )
    """
    allure.dynamic.issue(ISSUE)
    allure.dynamic.link(CUSTOM_LINK, link_type=CUSTOM_LINK_TYPE)
