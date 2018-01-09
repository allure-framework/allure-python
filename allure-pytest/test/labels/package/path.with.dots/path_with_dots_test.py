"""
>>> allure_report = getfixture('allure_report')
"""


def test_path_with_dots():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_path_with_dots',
    ...                           has_package(
    ...                                       ends_with('path.with.dots.path_with_dots_test'),
    ...                           ),
    ...             )
    ... )
    """
    pass
