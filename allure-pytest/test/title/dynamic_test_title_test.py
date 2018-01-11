import allure


@allure.title("A some test tile")
def test_dynamic_title():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_dynamic_title',
    ...                           has_title("It is renamed test")
    ...             )
    ... )
    """
    allure.dynamic.title("It is renamed test")
