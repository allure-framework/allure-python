def test_default_suite_function():
    """
    >>> from hamcrest import not_, anything
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_default_suite_function',
    ...                           has_parent_suite('test.labels.suite'),
    ...                           has_suite('function_suite_test'),
    ...                           not_(has_sub_suite(anything()))
    ...             )
    ... )

    """
    pass
