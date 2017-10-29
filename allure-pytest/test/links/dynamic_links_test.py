import pytest
import allure

LINK_1 = "https://github.com"
LINK_2 = "https://gitter.im"


@allure.link(LINK_1)
def test_dynamic_links():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_dynamic_links',
    ...                           has_link(LINK_1),
    ...                           has_link(LINK_2)
    ...             ))
    """
    allure.dynamic.link(LINK_2)


@pytest.mark.parametrize('link', (LINK_1, LINK_2))
def test_parametrized_dynamic_links(link):
    """
    >>> allure_report = getfixture('allure_report')
    >>> for link in [LINK_1, LINK_2]:
    ...     assert_that(allure_report,
    ...                 has_test_case('test_parametrized_dynamic_links[{link}]'.format(link=link),
    ...                               has_link(link)
    ...                 )
    ...     )
    """
    allure.dynamic.link(link)
