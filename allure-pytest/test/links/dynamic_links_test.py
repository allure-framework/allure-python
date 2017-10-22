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
