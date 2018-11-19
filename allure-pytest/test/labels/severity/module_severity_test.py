"""
>>> allure_report = getfixture('allure_report')
>>> assert_that(allure_report,
...             all_of(
...                 has_property('test_cases', has_length(4)),
...                 has_property('test_groups', has_length(0))
...             ))  # doctest: +SKIP
"""

import allure

pytestmark = allure.severity(allure.severity_level.TRIVIAL)


def test_not_decorated_function():
    """
    >>> allure_report = getfixture('allure_report')
    >>> assert_that(allure_report,
    ...             has_test_case('test_not_decorated_function',
    ...                           has_severity('trivial')
    ...             )
    ... )
    """
    pass


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


class TestNotDecorated(object):

    def test_method_of_not_decorated_class(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_method_of_not_decorated_class',
        ...                           has_severity('trivial')
        ...             )
        ... )
        """
        pass


@allure.severity(allure.severity_level.NORMAL)
class TestDecorated(object):

    def test_method_of_decorated_class(self):
        """
        >>> allure_report = getfixture('allure_report')
        >>> assert_that(allure_report,
        ...             has_test_case('test_method_of_decorated_class',
        ...                           has_severity('normal')
        ...             )
        ... )
        """
        pass
