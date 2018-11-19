import allure


@allure.severity(allure.severity_level.MINOR)
def test_decorated_function():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_decorated_function',
    ...                           has_severity('minor')
    ...             )
    ... )

    """
    pass


#@pytest.allure.CRITICAL
def Xtest_short_decorated_function():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_short_decorated_function',
    ...                           has_severity('critical')
    ...             )
    ... ) # doctest: +SKIP

    """
    pass
